import { ensureCDP } from './cdp_utils.js';
import { SELECTORS } from '../selectors.js';

async function injectMessage(cdp, text) {
    const safeText = JSON.stringify(text);
    const EXP = `(async () => {
        const SELECTORS = ${JSON.stringify(SELECTORS)};
        
        function isSubmitButton(btn) {
            if (btn.disabled || btn.offsetWidth === 0) return false;
            const svg = btn.querySelector('svg');
            if (svg) {
                const cls = (svg.getAttribute('class') || '') + ' ' + (btn.getAttribute('class') || '');
                if (SELECTORS.SUBMIT_BUTTON_SVG_CLASSES.some(c => cls.includes(c))) return true;
            }
            return false;
        }

        const doc = document;
        const els = doc.querySelectorAll(SELECTORS.CHAT_INPUT);
        const editor = Array.from(els).filter(el => el.offsetParent !== null).at(-1);
        
        if (!editor) return { ok: false, error: "No editor found" };

        editor.focus();
        document.execCommand("insertText", false, ${safeText});
        editor.dispatchEvent(new Event('input', { bubbles: true }));
        
        await new Promise(r => setTimeout(r, 500));

        const buttons = Array.from(doc.querySelectorAll(SELECTORS.SUBMIT_BUTTON_CONTAINER));
        const submit = buttons.find(isSubmitButton);
        
        if (submit) {
             submit.click();
             return { ok: true, method: "click" };
        }
        
        editor.dispatchEvent(new KeyboardEvent("keydown", { bubbles:true, key:"Enter", code:"Enter", keyCode: 13 }));
        return { ok: true, method: "enter" };
    })()`;

    for (const ctx of cdp.contexts) {
        try {
            const res = await cdp.call("Runtime.evaluate", { expression: EXP, returnByValue: true, awaitPromise: true, contextId: ctx.id });
            if (res.result?.value?.ok) return res.result.value;
        } catch (e) { }
    }
    return { ok: false, error: "Injection failed" };
}

async function startNewChat(cdp) {
    const EXP = `(() => {
        const selectors = [
            '[data-tooltip-id="new-conversation-tooltip"]',
            '[data-tooltip-id*="new-chat"]',
            '[aria-label*="New Chat"]'
        ];
        
        for (const sel of selectors) {
            const btn = document.querySelector(sel);
            if (btn) {
                const dispatch = (type, Cls) => {
                    const ev = new Cls(type, { bubbles: true, cancelable: true, view: window, buttons: 1 });
                    btn.dispatchEvent(ev);
                };
                dispatch('pointerdown', PointerEvent);
                dispatch('mousedown', MouseEvent);
                dispatch('pointerup', PointerEvent);
                dispatch('mouseup', MouseEvent);
                dispatch('click', MouseEvent);
                btn.click();
                return { success: true, method: sel };
            }
        }
        return { success: false };
    })()`;
    for (const ctx of cdp.contexts) {
        try {
            const res = await cdp.call("Runtime.evaluate", { expression: EXP, returnByValue: true, contextId: ctx.id });
            if (res.result?.value?.success) return res.result.value;
        } catch (e) { }
    }
    return { success: false };
}

async function getChatSnapshot(cdp) {
    const EXP = `(() => {
        const titleEl = document.querySelector('p.text-ide-sidebar-title-color');
        return {
            messageCount: document.querySelectorAll('[data-message-role]').length,
            title: titleEl ? (titleEl.innerText || '').trim() : null
        };
    })()`;

    for (const ctx of cdp.contexts) {
        try {
            const res = await cdp.call("Runtime.evaluate", { expression: EXP, returnByValue: true, contextId: ctx.id });
            if (res.result?.value) return res.result.value;
        } catch (e) { }
    }
    return { messageCount: 0, title: null };
}

async function runTest() {
    console.log("=== Testing Meaningful New Chat Workflow ===");
    const cdp = await ensureCDP();
    if (!cdp) {
        console.error("[ERROR] CDP connection failed.");
        process.exit(1);
    }

    const before = await getChatSnapshot(cdp);
    console.log(`[INFO] Before new chat: title="${before.title || 'null'}", messages=${before.messageCount}`);

    // 1. Perform "New Chat" reset first to start fresh
    console.log("[INFO] Starting a New Chat to clear the workspace...");
    const resetResult = await startNewChat(cdp);

    if (resetResult.success) {
        console.log(`[SUCCESS] New chat signal sent via: ${resetResult.method}`);
        console.log("[INFO] Waiting for reset to clear UI...");
        await new Promise(r => setTimeout(r, 4000));
        const afterReset = await getChatSnapshot(cdp);
        console.log(`[INFO] After new chat: title="${afterReset.title || 'null'}", messages=${afterReset.messageCount}`);

        // 2. Inject a meaningful construction prompt
        console.log("[INFO] Injecting instruction to build a Dice App...");
        const appPrompt = "このWorkspaceに、シンプルなサイコロアプリ（HTML/JS）を作ってください。";
        const injectResult = await injectMessage(cdp, appPrompt);

        if (injectResult.ok) {
            console.log(`[SUCCESS] Generation prompt submitted via ${injectResult.method}.`);
            console.log("[INFO] Waiting 15 seconds to observe the agent starting work...");
            await new Promise(r => setTimeout(r, 15000));

            // Verify activity
            const EXP = `document.querySelectorAll('[data-message-role]').length`;
            let count = 0;
            for (const ctx of cdp.contexts) {
                try {
                    const res = await cdp.call("Runtime.evaluate", { expression: EXP, returnByValue: true, contextId: ctx.id });
                    if (res.result?.value > 0) { count = res.result.value; break; }
                } catch (e) { }
            }
            console.log(`[INFO] Current message count: ${count}`);
            if (count > 0) {
                console.log("[SUCCESS] VERIFIED: New Chat + App Generation is working correctly!");
            } else {
                console.error("[FAILED] No messages detected. New chat flow is not verified.");
                process.exit(1);
            }
        } else {
            console.error(`[FAILED] Failed to submit application prompt: ${injectResult.error}`);
            process.exit(1);
        }
    } else {
        console.error(`[FAILED] New Chat button not found.`);
        process.exit(1);
    }

    console.log("Test finished.");
    process.exit(0);
}

runTest();
