workspace(name = "com_github_buildbuddy_io_rules_xcodeproj")

load("//xcodeproj:repositories.bzl", "xcodeproj_rules_dependencies")

xcodeproj_rules_dependencies(use_dev_patches = True)

load(
    "@build_bazel_rules_apple//apple:repositories.bzl",
    "apple_rules_dependencies",
)

apple_rules_dependencies()

load(
    "@build_bazel_rules_swift//swift:repositories.bzl",
    "swift_rules_dependencies",
)

swift_rules_dependencies()

load(
    "@build_bazel_rules_swift//swift:extras.bzl",
    "swift_rules_extra_dependencies",
)

swift_rules_extra_dependencies()

# Setup Swift Custom Dump test dependency

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "com_github_pointfreeco_xctest_dynamic_overlay",
    build_file_content = """\
load("@build_bazel_rules_swift//swift:swift.bzl", "swift_library")

swift_library(
    name = "XCTestDynamicOverlay",
    module_name = "XCTestDynamicOverlay",
    srcs = glob(["Sources/XCTestDynamicOverlay/**/*.swift"]),
    visibility = ["//visibility:public"],
)
""",
    sha256 = "97169124feb98b409f5b890bd95bb147c2fba0dba3098f9bf24c539270ee9601",
    strip_prefix = "xctest-dynamic-overlay-0.2.1",
    url = "https://github.com/pointfreeco/xctest-dynamic-overlay/archive/refs/tags/0.2.1.tar.gz",
)

http_archive(
    name = "com_github_pointfreeco_swift_custom_dump",
    build_file_content = """\
load("@build_bazel_rules_swift//swift:swift.bzl", "swift_library")

swift_library(
    name = "CustomDump",
    module_name = "CustomDump",
    srcs = glob(["Sources/CustomDump/**/*.swift"]),
    deps = ["@com_github_pointfreeco_xctest_dynamic_overlay//:XCTestDynamicOverlay"],
    visibility = ["//visibility:public"],
)
""",
    patches = [
        # Custom for our tests
        "//third_party/com_github_pointfreeco_swift_custom_dump:type_name.patch",
    ],
    sha256 = "a45e8f275794960651043623e23abb8365f0455b4ad5976bc56a4fa00c5efb31",
    strip_prefix = "swift-custom-dump-0.5.0",
    url = "https://github.com/pointfreeco/swift-custom-dump/archive/refs/tags/0.5.0.tar.gz",
)

# Setup the Skylib dependency, this is required to use the Starlark unittest
# framework. Since this is only used for rules_xcodeproj's tests, we configure
# it here in the WORKSPACE file. This also can't be added to
# `xcodeproj_rules_dependencies` since we need to load the bzl file, so if we
# wanted to load it inside of a macro, it would need to be in a different file
# to begin with.
load("@bazel_skylib//:workspace.bzl", "bazel_skylib_workspace")

bazel_skylib_workspace()

# Buildifier

http_archive(
    name = "buildifier_prebuilt",
    sha256 = "0450069a99db3d414eff738dd8ad4c0969928af13dc8614adbd1c603a835caad",
    strip_prefix = "buildifier-prebuilt-0.4.0",
    urls = [
        "http://github.com/keith/buildifier-prebuilt/archive/0.4.0.tar.gz",
    ],
)

load("@buildifier_prebuilt//:deps.bzl", "buildifier_prebuilt_deps")

buildifier_prebuilt_deps()

load("@buildifier_prebuilt//:defs.bzl", "buildifier_prebuilt_register_toolchains")

buildifier_prebuilt_register_toolchains()

# Stardoc

http_archive(
    name = "io_bazel_stardoc",
    sha256 = "05fb57bb4ad68a360470420a3b6f5317e4f722839abc5b17ec4ef8ed465aaa47",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/stardoc/releases/download/0.5.2/stardoc-0.5.2.tar.gz",
        "https://github.com/bazelbuild/stardoc/releases/download/0.5.2/stardoc-0.5.2.tar.gz",
    ],
)

load("@io_bazel_stardoc//:setup.bzl", "stardoc_repositories")

stardoc_repositories()
