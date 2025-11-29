import Foundation

struct SignInRequest: Encodable {
    var username: String
    var password: String
    var phoneModel: String = "string"
    var operationalSystem: String = "string"
}

struct SignUpRequest: Encodable {
    var username: String
    var password: String
}

struct User: Decodable {
    var username: String
//    var balance:
}

struct UserProfileResponse: Decodable {
    let name: String
}

struct AuthResponse: Codable {
    let token: String
}

enum AuthError: Error {
    case invalidURL
    case noResponse
    case server(Int)
}

