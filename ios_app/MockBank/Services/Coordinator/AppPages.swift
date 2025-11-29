import Foundation

enum AppPages: Hashable {
    case signIn
    case signUp
    case main
    case transactions(username: String)
}

enum Sheet: Identifiable {
    var id: String {
        switch self {
        case .sendFunds: return "addFunds"
        }
    }
    
    case sendFunds(sender: String)
}

enum FullScreenCover: String, Identifiable {
    var id: String {
        self.rawValue
    }
    
    case transactions
}
