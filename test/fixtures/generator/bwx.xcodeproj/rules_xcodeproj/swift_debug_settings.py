#!/usr/bin/python3

"""An lldb module that registers a stop hook to set swift settings."""

import lldb

_BUNDLE_EXTENSIONS = [
    ".app",
    ".appex",
    ".bundle",
    ".framework",
    ".xctest",
]

_SETTINGS = {
  "x86_64-apple-macosx12.0.0 generator" : {
    "clang" : "-iquote \"$(PROJECT_DIR)\" -iquote \"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin\" -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote \"$(PROJECT_DIR)\" -iquote \"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin\" -O0 -fstack-protector -fstack-protector-all -iquote \"$(PROJECT_DIR)\" -iquote \"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin\" -O0 -fstack-protector -fstack-protector-all -iquote \"$(PROJECT_DIR)\" -iquote \"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin\" -O0 -fstack-protector -fstack-protector-all -iquote \"$(PROJECT_DIR)\" -iquote \"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin\" -O0 -fstack-protector -fstack-protector-all",
    "frameworks" : [

    ],
    "includes" : [
      "$(BUILD_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin/external/com_github_apple_swift_collections",
      "$(BUILD_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin/external/com_github_tuist_xcodeproj",
      "$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin/external/com_github_tadija_aexml",
      "$(BUILD_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin/external/com_github_kylef_pathkit"
    ]
  },
  "x86_64-apple-macosx12.0.0 tests.xctest/Contents/MacOS/tests" : {
    "clang" : "-iquote \"$(PROJECT_DIR)\" -iquote \"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin\" -O0 -DDEBUG=1 -fstack-protector -fstack-protector-all -iquote \"$(PROJECT_DIR)\" -iquote \"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin\" -O0 -fstack-protector -fstack-protector-all -iquote \"$(PROJECT_DIR)\" -iquote \"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin\" -O0 -fstack-protector -fstack-protector-all -iquote \"$(PROJECT_DIR)\" -iquote \"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin\" -O0 -fstack-protector -fstack-protector-all -iquote \"$(PROJECT_DIR)\" -iquote \"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin\" -O0 -fstack-protector -fstack-protector-all -iquote \"$(PROJECT_DIR)\" -iquote \"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin\" -O0 -fstack-protector -fstack-protector-all -iquote \"$(PROJECT_DIR)\" -iquote \"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin\" -O0 -fstack-protector -fstack-protector-all -iquote \"$(PROJECT_DIR)\" -iquote \"$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin\" -O0 -fstack-protector -fstack-protector-all",
    "frameworks" : [
      "$(PLATFORM_DIR)/Developer/Library/Frameworks",
      "$(SDKROOT)/Developer/Library/Frameworks"
    ],
    "includes" : [
      "$(PLATFORM_DIR)/Developer/usr/lib",
      "$(BUILD_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin/tools/generator",
      "$(BUILD_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin/external/com_github_pointfreeco_swift_custom_dump",
      "$(BUILD_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin/external/com_github_apple_swift_collections",
      "$(BUILD_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin/external/com_github_tuist_xcodeproj",
      "$(BAZEL_OUT)/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin/external/com_github_tadija_aexml",
      "$(BUILD_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin/external/com_github_kylef_pathkit",
      "$(BUILD_DIR)/bazel-out/macos-x86_64-min12.0-applebin_macos-darwin_x86_64-dbg-ST-0c83c5e59889/bin/external/com_github_pointfreeco_xctest_dynamic_overlay"
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
        module_name = module.file.__get_fullpath__()
        target_triple = module.GetTriple()
        executable_path = _get_relative_executable_path(module_name)
        key = f"{target_triple} {executable_path}"

        settings = _SETTINGS.get(key)

        if settings:
            frameworks = " ".join([
                f'"{path}"'
                for path in settings["frameworks"]
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
                for path in settings["includes"]
            ])
            if includes:
                lldb.debugger.HandleCommand(
                    f"settings set -- target.swift-module-search-paths {includes}",
                )
            else:
                lldb.debugger.HandleCommand(
                    "settings clear target.swift-module-search-paths",
                )

            clang = settings["clang"]
            if clang:
                lldb.debugger.HandleCommand(
                    f"settings set -- target.swift-extra-clang-flags '{clang}'",
                )
            else:
                lldb.debugger.HandleCommand(
                    "settings clear target.swift-extra-clang-flags",
                )

        return True
