"""Implementation of the `default_automatic_target_processing_aspect` aspect."""

load(
    "@build_bazel_rules_apple//apple:providers.bzl",
    "AppleBinaryInfo",
    "AppleBundleInfo",
    "AppleFrameworkImportInfo",
    "AppleResourceBundleInfo",
)
load(":providers.bzl", "XcodeProjAutomaticTargetProcessingInfo", "target_type")

# Utility

_UNSUPPORTED_SRCS_EXTENSIONS = {
    "a": True,
    "lo": True,
    "o": True,
    "so": True,
}

def _get_target_type(*, target):
    # Top-level bundles
    if AppleBundleInfo in target:
        return target_type.compile

    # Resource bundles
    if AppleResourceBundleInfo in target:
        return None

    # Libraries
    if CcInfo in target:
        return target_type.compile

    # Command-line tools
    executable = target[DefaultInfo].files_to_run.executable
    if executable and not executable.is_source:
        return target_type.compile

    return None

def _is_test_target(target):
    """Returns whether the given target is for test purposes or not."""
    if AppleBundleInfo not in target:
        return False
    return target[AppleBundleInfo].product_type in (
        "com.apple.product-type.bundle.ui-testing",
        "com.apple.product-type.bundle.unit-test",
    )

# Aspects

def _default_automatic_target_processing_aspect_impl(target, ctx):
    if XcodeProjAutomaticTargetProcessingInfo in target:
        return []

    this_target_type = _get_target_type(target = target)

    # Targets that don't produce outputs can't be Xcode targets
    # TODO: Limit this to archives, bundles, executables, and swiftmodules?
    should_generate_target = target.files != depset()

    if CcInfo in target:
        srcs = ["srcs"]
    else:
        srcs = []

    app_icons = None
    bundle_id = None
    codesignopts = None
    deps = ["deps"]
    entitlements = None
    exported_symbols_lists = []
    infoplists = []
    launchdplists = []
    bazel_build_mode_error = None
    non_arc_srcs = []
    pch = None
    provisioning_profile = None

    attrs = dir(ctx.rule.attr)

    if ctx.rule.kind == "cc_library":
        xcode_targets = {
            "deps": [target_type.compile, None],
            "interface_deps": [target_type.compile],
        }
    elif ctx.rule.kind == "objc_library":
        xcode_targets = {
            "deps": [target_type.compile, None],
            "runtime_deps": [target_type.compile],
        }
        non_arc_srcs = ["non_arc_srcs"]
        pch = "pch"
    elif ctx.rule.kind == "swift_library":
        xcode_targets = {
            "deps": [target_type.compile, None],
            "private_deps": [target_type.compile, None],
        }
    elif ctx.rule.kind == "apple_resource_bundle":
        xcode_targets = {}

        # Ideally this would be exposed on `AppleResourceBundleInfo`
        bundle_id = "bundle_id"
        infoplists = ["infoplists"]
        should_generate_target = False
    elif AppleBundleInfo in target:
        xcode_targets = {
            "deps": [target_type.compile, None],
        }
        if _is_test_target(target):
            xcode_targets["test_host"] = [target_type.compile]
        if "app_clips" in attrs:
            xcode_targets["app_clips"] = [target_type.compile]
        if "app_icons" in attrs:
            app_icons = "app_icons"
        if "codesignopts" in attrs:
            codesignopts = "codesignopts"
        if "entitlements" in attrs:
            entitlements = "entitlements"
        if "extension" in attrs:
            xcode_targets["extension"] = [target_type.compile]
        if "extensions" in attrs:
            xcode_targets["extensions"] = [target_type.compile]
        if "infoplists" in attrs:
            infoplists = ["infoplists"]
        if "provisioning_profile" in attrs:
            provisioning_profile = "provisioning_profile"
        if "watch_application" in attrs:
            xcode_targets["watch_application"] = [target_type.compile]
    elif AppleBinaryInfo in target:
        if "binary" in attrs:
            deps_attr = "binary"
        else:
            deps_attr = "deps"
        deps = [deps_attr]

        if "codesignopts" in attrs:
            codesignopts = "codesignopts"
        if "exported_symbols_lists" in attrs:
            exported_symbols_lists = ["exported_symbols_lists"]
        if "infoplists" in attrs:
            infoplists = ["infoplists"]
        if "launchdplists" in attrs:
            launchdplists = ["launchdplists"]
        xcode_targets = {
            deps_attr: [target_type.compile, None],
        }
    elif AppleFrameworkImportInfo in target:
        xcode_targets = {"deps": [target_type.compile]}
        if getattr(ctx.rule.attr, "bundle_only", False):
            bazel_build_mode_error = """\
`bundle_only` can't be `True` on {} when `build_mode = \"xcode\"`
""".format(target.label)

        should_generate_target = False
    else:
        xcode_targets = {
            "deps": [this_target_type, None],
        }

        # Command-line tools
        executable = target[DefaultInfo].files_to_run.executable
        is_executable = executable and not executable.is_source

        should_generate_target = is_executable
        if is_executable and "srcs" in attrs:
            srcs = ["srcs"]

    # Xcode doesn't support some source types that Bazel supports
    for attr in srcs:
        for file in getattr(ctx.rule.files, attr, []):
            if _UNSUPPORTED_SRCS_EXTENSIONS.get(file.extension):
                should_generate_target = False
                break

    return [
        XcodeProjAutomaticTargetProcessingInfo(
            app_icons = app_icons,
            bazel_build_mode_error = bazel_build_mode_error,
            bundle_id = bundle_id,
            codesignopts = codesignopts,
            deps = deps,
            entitlements = entitlements,
            exported_symbols_lists = exported_symbols_lists,
            infoplists = infoplists,
            launchdplists = launchdplists,
            non_arc_srcs = non_arc_srcs,
            pch = pch,
            provisioning_profile = provisioning_profile,
            should_generate_target = should_generate_target,
            srcs = srcs,
            target_type = this_target_type,
            xcode_targets = xcode_targets,
        ),
    ]

default_automatic_target_processing_aspect = aspect(
    implementation = _default_automatic_target_processing_aspect_impl,
    attr_aspects = ["*"],
)
