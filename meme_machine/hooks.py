import modules.credits.hooks as credit_hooks

# Passes (client, message) to every function
HOOK_USER_MESSAGE_SENT = [
    *credit_hooks.HOOK_USER_MESSAGE_SENT
]
