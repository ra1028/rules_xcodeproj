import XcodeProj
import XCTest

@testable import generator

// MARK: - Host Resolution Tests

extension XCSchemeInfoBuildActionInfoTests {
    func test_hostResolution_noBuildActionInfo() throws {
        let actionInfo = try XCSchemeInfo.BuildActionInfo(
            resolveHostsFor: nil,
            topLevelTargetInfos: topLevelTargetInfos
        )
        XCTAssertNil(actionInfo)
    }

    func test_hostResolution_withBuildActionInfo() throws {
        let actionInfo = try XCSchemeInfo.BuildActionInfo(
            resolveHostsFor: .init(
                targets: [unresolvedLibraryTargetInfoWithHosts].map {
                    .init(targetInfo: $0, buildFor: .allEnabled)
                }
            ),
            topLevelTargetInfos: topLevelTargetInfos
        )
        guard let buildActionInfo = actionInfo else {
            XCTFail("Expected a `BuildActionInfo`")
            return
        }
        // We could check for the host resolution not equal to .unresolved. However, by checking for
        // a specific selected host, we are sure that the topLevelTargetInfos was passed along
        // correctly.
        guard let targetInfo = buildActionInfo.targets.first?.targetInfo else {
            XCTFail("Expected a `TargetInfo`")
            return
        }
        let selectedHostInfo = try targetInfo.selectedHostInfo
        XCTAssertEqual(selectedHostInfo, unitTestHostInfo)
    }
}

// MARK: - Custom Scheme Initializer Tests

extension XCSchemeInfoBuildActionInfoTests {
    func test_customSchemeInit_withBuildAction() throws {
        // To keep this test simple, we are passing in the pre-defaults version of `BuildAction`.
        // Hence, the "A 2" target from the scheme will not appear in the `BuildAction`.
        let actual = try XCSchemeInfo.BuildActionInfo(
            buildAction: xcodeScheme.buildAction,
            targetResolver: targetResolver,
            targetIDsByLabel: try xcodeScheme.resolveTargetIDs(
                targetResolver: targetResolver,
                xcodeprojBazelLabel: xcodeprojBazelLabel
            )
        )
        let expected = try XCSchemeInfo.BuildActionInfo(
            targets: [
                .init(
                    targetInfo: try targetResolver.targetInfo(targetID: "A 1"),
                    buildFor: .allEnabled
                ),
            ]
        )
        XCTAssertEqual(actual, expected)
    }
}

// MARK: - Test Data

class XCSchemeInfoBuildActionInfoTests: XCTestCase {
    let xcodeprojBazelLabel = BazelLabel("//foo")

    lazy var filePathResolver = FilePathResolver(
        workspaceDirectory: "/Users/TimApple/app",
        externalDirectory: "/some/bazel4/external",
        bazelOutDirectory: "/some/bazel4/bazel-out",
        internalDirectoryName: "rules_xcodeproj",
        workspaceOutputPath: "examples/foo/Foo.xcodeproj"
    )

    lazy var targetResolver = Fixtures.targetResolver(
        referencedContainer: filePathResolver.containerReference
    )

    lazy var pbxTargetsDict = targetResolver.pbxTargets

    lazy var libraryPlatform = Fixtures.targets["A 1"]!.platform
    lazy var appPlatform = Fixtures.targets["A 2"]!.platform
    lazy var unitTestPlatform = Fixtures.targets["B 2"]!.platform

    lazy var libraryPBXTarget = pbxTargetsDict["A 1"]!
    lazy var appPBXTarget = pbxTargetsDict["A 2"]!
    lazy var unitTestPBXTarget = pbxTargetsDict["B 2"]!

    lazy var appHostInfo = XCSchemeInfo.HostInfo(
        pbxTarget: appPBXTarget,
        platforms: [appPlatform],
        referencedContainer: filePathResolver.containerReference,
        index: 0
    )
    lazy var unitTestHostInfo = XCSchemeInfo.HostInfo(
        pbxTarget: unitTestPBXTarget,
        platforms: [unitTestPlatform],
        referencedContainer: filePathResolver.containerReference,
        index: 1
    )

    lazy var unresolvedLibraryTargetInfoWithHosts = XCSchemeInfo.TargetInfo(
        pbxTarget: libraryPBXTarget,
        platforms: [libraryPlatform],
        referencedContainer: filePathResolver.containerReference,
        hostInfos: [appHostInfo, unitTestHostInfo],
        extensionPointIdentifiers: []
    )

    lazy var topLevelTargetInfos: [XCSchemeInfo.TargetInfo] = [
        .init(
            pbxTarget: unitTestPBXTarget,
            platforms: [unitTestPlatform],
            referencedContainer: filePathResolver.containerReference,
            hostInfos: [],
            extensionPointIdentifiers: []
        ),
    ]

    lazy var xcodeScheme = try! XcodeScheme(
        name: "My Scheme",
        // swiftlint:disable:next force_try
        buildAction: try! .init(targets: [.init(label: targetResolver.targets["A 1"]!.label)]),
        launchAction: .init(target: targetResolver.targets["A 2"]!.label)
    )
}
