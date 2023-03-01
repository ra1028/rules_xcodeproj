#!/usr/bin/python3

"""An lldb module that registers a stop hook to set swift settings."""

import lldb
import re

# Order matters, it needs to be from the most nested to the least
_BUNDLE_EXTENSIONS = [
    ".framework",
    ".xctest",
    ".appex",
    ".bundle",
    ".app",
]

_TRIPLE_MATCH = re.compile(r"([^-]+-[^-]+)(-\D+)[^-]*(-.*)?")

_SETTINGS = {
	"x86_64-apple-macosx generator": {
		"c": "-I$(PROJECT_DIR)/external/com_github_michaeleisel_jjliso8601dateformatter/Sources/JJLISO8601DateFormatter/include -I$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_jjliso8601dateformatter/Sources/JJLISO8601DateFormatter/include -I$(PROJECT_DIR)/external/com_github_michaeleisel_zippyjsoncfamily/Sources/ZippyJSONCFamily/include -I$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_zippyjsoncfamily/Sources/ZippyJSONCFamily/include -iquote$(PROJECT_DIR)/external/com_github_michaeleisel_jjliso8601dateformatter -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_jjliso8601dateformatter -iquote$(PROJECT_DIR)/external/com_github_michaeleisel_zippyjsoncfamily -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_zippyjsoncfamily -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_jjliso8601dateformatter/JJLISO8601DateFormatter.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_zippyjsoncfamily/ZippyJSONCFamily.swift.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_michaeleisel_jjliso8601dateformatter -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_jjliso8601dateformatter -iquote$(PROJECT_DIR)/external/com_github_michaeleisel_zippyjsoncfamily -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_zippyjsoncfamily -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all",
		"s": [
			"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_apple_swift_collections",
			"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_zippyjson",
			"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_tuist_xcodeproj",
			"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_tadija_aexml",
			"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_kylef_pathkit"
		]
	},
	"x86_64-apple-macosx swiftc": {
		"c": "-iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all"
	},
	"x86_64-apple-macosx tests.xctest/Contents/MacOS/tests": {
		"c": "-I$(PROJECT_DIR)/external/com_github_michaeleisel_jjliso8601dateformatter/Sources/JJLISO8601DateFormatter/include -I$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_jjliso8601dateformatter/Sources/JJLISO8601DateFormatter/include -I$(PROJECT_DIR)/external/com_github_michaeleisel_zippyjsoncfamily/Sources/ZippyJSONCFamily/include -I$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_zippyjsoncfamily/Sources/ZippyJSONCFamily/include -iquote$(PROJECT_DIR)/external/com_github_michaeleisel_jjliso8601dateformatter -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_jjliso8601dateformatter -iquote$(PROJECT_DIR)/external/com_github_michaeleisel_zippyjsoncfamily -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_zippyjsoncfamily -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_jjliso8601dateformatter/JJLISO8601DateFormatter.swift.modulemap -fmodule-map-file=$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_zippyjsoncfamily/ZippyJSONCFamily.swift.modulemap -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_michaeleisel_jjliso8601dateformatter -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_jjliso8601dateformatter -iquote$(PROJECT_DIR)/external/com_github_michaeleisel_zippyjsoncfamily -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_zippyjsoncfamily -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR)/external/com_github_michaeleisel_jjliso8601dateformatter -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_jjliso8601dateformatter -iquote$(PROJECT_DIR)/external/com_github_michaeleisel_zippyjsoncfamily -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_zippyjsoncfamily -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all -iquote$(PROJECT_DIR) -iquote$(PROJECT_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin -O0 -fstack-protector -fstack-protector-all",
		"f": [
			"$(DEVELOPER_DIR)/Platforms/MacOSX.platform/Developer/Library/Frameworks"
		],
		"s": [
			"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/tools/generator",
			"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_pointfreeco_swift_custom_dump",
			"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_apple_swift_collections",
			"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_michaeleisel_zippyjson",
			"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_tuist_xcodeproj",
			"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_tadija_aexml",
			"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_kylef_pathkit",
			"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-STABLE-1/bin/external/com_github_pointfreeco_xctest_dynamic_overlay"
		]
	}
}

def __lldb_init_module(debugger, _internal_dict):
    # Register the stop hook when this module is loaded in lldb
    ci = debugger.GetCommandInterpreter()
    res = lldb.SBCommandReturnObject()
    ci.HandleCommand(
        "target stop-hook add -P swift_debug_settings.StopHook",
        res,
    )
    if not res.Succeeded():
        print(f"""\
Failed to register Swift debug options stop hook:

{res.GetError()}
Please file a bug report here: \
https://github.com/buildbuddy-io/rules_xcodeproj/issues/new?template=bug.md
""")
        return

def _get_relative_executable_path(module):
    for extension in _BUNDLE_EXTENSIONS:
        prefix, _, suffix = module.rpartition(extension)
        if prefix:
            return prefix.split("/")[-1] + extension + suffix
    return module.split("/")[-1]

class StopHook:
    "An lldb stop hook class, that sets swift settings for the current module."

    def __init__(self, _target, _extra_args, _internal_dict):
        pass

    def handle_stop(self, exe_ctx, _stream):
        "Method that is called when the user stops in lldb."
        module = exe_ctx.frame.module
        if not module:
            return

        module_name = module.file.__get_fullpath__()
        versionless_triple = _TRIPLE_MATCH.sub(r"\1\2\3", module.GetTriple())
        executable_path = _get_relative_executable_path(module_name)
        key = f"{versionless_triple} {executable_path}"

        settings = _SETTINGS.get(key)

        if settings:
            frameworks = " ".join([
                f'"{path}"'
                for path in settings.get("f", [])
            ])
            if frameworks:
                lldb.debugger.HandleCommand(
                    f"settings set -- target.swift-framework-search-paths {frameworks}",
                )
            else:
                lldb.debugger.HandleCommand(
                    "settings clear target.swift-framework-search-paths",
                )

            includes = " ".join([
                f'"{path}"'
                for path in settings.get("s", [])
            ])
            if includes:
                lldb.debugger.HandleCommand(
                    f"settings set -- target.swift-module-search-paths {includes}",
                )
            else:
                lldb.debugger.HandleCommand(
                    "settings clear target.swift-module-search-paths",
                )

            clang = settings.get("c")
            if clang:
                lldb.debugger.HandleCommand(
                    f"settings set -- target.swift-extra-clang-flags '{clang}'",
                )
            else:
                lldb.debugger.HandleCommand(
                    "settings clear target.swift-extra-clang-flags",
                )

        return True