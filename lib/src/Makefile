CFLAGS ?= -Os -Wall

PYTHON        ?= python3
PKG_MODULES   := pygobject-3.0 webkit2gtk-web-extension-4.0 ${PYTHON}
WEB_EXT_FLAGS := $(shell pkg-config ${PKG_MODULES} --cflags)
WEB_EXT_LIBS  := $(shell pkg-config ${PKG_MODULES} --libs)

CPPFLAGS += ${WEB_EXT_FLAGS}
LDLIBS   += ${WEB_EXT_LIBS}

all: extension.so

extension.so: extension.o
	${LD} ${LDFLAGS} -fPIC -shared -o $@ $^ ${LDLIBS}
extension.so: CFLAGS += -fPIC

clean:
	${RM} extension.o extension.so

# vim:ft=make
#
