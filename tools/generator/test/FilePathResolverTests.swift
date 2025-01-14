import PathKit
import XCTest

@testable import generator

class FilePathResolverTests: XCTestCase {
    let workspaceDirectory: Path = "/Users/TimApple/project"
    let externalDirectory: Path = "/some/bazel2/external"
    let bazelOutDirectory: Path = "/some/bazel2/bazel-out"
    let internalDirectoryName = "internal_name"
    let workspaceOutputPath: Path = "path/to/Foo.xcodeproj"
    lazy var resolver = FilePathResolver(
        workspaceDirectory: workspaceDirectory,
        externalDirectory: externalDirectory,
        bazelOutDirectory: bazelOutDirectory,
        internalDirectoryName: internalDirectoryName,
        workspaceOutputPath: workspaceOutputPath
    )

    func test_containerReference() throws {
        XCTAssertEqual(
            resolver.containerReference,
            "container:\(workspaceOutputPath)"
        )
    }
}
