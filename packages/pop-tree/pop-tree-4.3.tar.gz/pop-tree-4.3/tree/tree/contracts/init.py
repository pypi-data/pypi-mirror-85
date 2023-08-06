def pre(hub, ctx):
    ...


def call(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def post(hub, ctx):
    return ctx.ret
