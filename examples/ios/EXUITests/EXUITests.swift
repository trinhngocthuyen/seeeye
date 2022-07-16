//
//  EXUITests.swift
//  EXUITests
//
//  Created by Ngoc Thuyen Trinh on 7/6/22.
//

import XCTest
@testable import EX

class EXUITests: XCTestCase {
  func testUI1() throws { }
  func testUI2() throws { }
  func testUI3() throws {
    // This logic is to simulate flaky test.
    // The test fails in the 1st run and succeeds in the 2nd run.
    // The attempt count is controlled by an external file (ignored by git)
    //     $(PWD)/tmp/test_retries_trace
    // Make sure you reset the content of this file to 0 beforehand.
    guard let path = ProcessInfo.processInfo.environment["RETRY_TRACE_PATH"],
          let text = try? String(contentsOfFile: path, encoding: .utf8),
          let count = Int(text)
    else { return }

    if count < 1 {
      try (count + 1).description.write(toFile: path, atomically: true, encoding: .utf8)
      XCTFail("Failed on purpose (count = \(count))")
    }
  }
}
