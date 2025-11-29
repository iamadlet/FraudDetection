import Foundation

protocol MainViewModelProtocol {
    func sendMoney(to recipient: String, amount: Double)
    func addMoney(amount: Double)
}

final class MainViewModel: ObservableObject {
    @Published var balance: Double = 10000
    @Published var username: String = ""
    @Published var lastThreeTransactions: [Transaction] = []
    @Published var isLoading: Bool = false
    
    private let transactionService: TransactionService
    private let authService: AuthService
    
    init(transactionService: TransactionService, authService: AuthService) {
        self.transactionService = transactionService
        self.authService = authService
    }
    
    func loadData() {
        isLoading = true
        
        let group = DispatchGroup()
        
        group.enter()
        authService.getCurrentUser { [weak self] result in
            defer { group.leave() }
            
            DispatchQueue.main.async {
                switch result {
                case .success(let profile):
                    self?.username = profile.name
                case .failure(let error):
                    print("User fetch error: \(error.localizedDescription)")
                }
            }
        }
        group.enter()
        transactionService.getAll { [weak self] result in
            defer { group.leave() }
            
            DispatchQueue.main.async {
                switch result {
                case .success(let transactions):
                    let sortedList = transactions.sorted { $0.date > $1.date }
                    self?.lastThreeTransactions = Array(sortedList.prefix(3))
                case .failure(let error):
                    print("Error loading transactions: \(error)")
                }
            }
        }
        
        group.notify(queue: .main) { [weak self] in
            self?.isLoading = false
            print("All data loaded")
        }
    }
    
    
    func formatBalance() -> String {
        String(format: "$%.2f", balance)
    }
}
