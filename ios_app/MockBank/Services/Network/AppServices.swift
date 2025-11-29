import Foundation

final class AppServices {
    static let shared = AppServices()
    private init() {}
    
    let authService = AuthService()
//    let transactionService = MockTransactionService()
    let transactionService = TransactionService(authTokenProvider: { KeychainManager.instance.getToken(forKey: "token") })
}
