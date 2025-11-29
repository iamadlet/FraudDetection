import Foundation

protocol TransactionsViewModelProtocol {
    func loadOperations()
}

final class TransactionsViewModel: ObservableObject {
    @Published var transactions: [Transaction] = []
    @Published var isLoading: Bool = false
    @Published var errorMessage: String? = nil
    
    let username: String
    
    private let service: TransactionService
    
    init(service: TransactionService, username: String) {
        self.service = service
        self.username = username
    }
    
    func loadData() {
        isLoading = true
        errorMessage = nil
        
        service.getAll { [weak self] result in
            DispatchQueue.main.async {
                self?.isLoading = false
                
                switch result {
                case .success(let data):
                    self?.transactions = data.sorted { $0.date > $1.date }
                case .failure(let error):
                    self?.errorMessage = error.localizedDescription
                    print("Error loading transactions: \(error.localizedDescription)")
                }
            }
        }
    }
}
