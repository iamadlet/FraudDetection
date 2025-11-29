import Foundation
import SwiftUI

class Coordinator: ObservableObject {
    @Published var path: NavigationPath = NavigationPath()
    @Published var fullScreenCover: FullScreenCover?
    @Published var sheet: Sheet?
    @Published var isAuthenticated: Bool = false
    
    private let services = AppServices.shared
    private let authService = AppServices.shared.authService
    
    init() {
        self.isAuthenticated = authService.getSavedToken() != nil
    }
    
    func signIn() {
        withAnimation {
            isAuthenticated = true
        }
    }
    
    func signOut() {
        authService.logout()
        withAnimation {
            isAuthenticated = false
            path = NavigationPath()
        }
    }
    
    func push(page: AppPages) {
        path.append(page)
    }
    
    func pop() {
        path.removeLast(path.count)
    }
    
    func presentSheet(_ sheet: Sheet) {
        self.sheet = sheet
    }
    
    func dismissSheet() {
        self.sheet = nil
    }
    
    func presentFullScreenCover(_ cover: FullScreenCover) {
        self.fullScreenCover = cover
    }
    
    func dismissCover() {
        self.fullScreenCover = nil
    }
    
    @ViewBuilder
    func build(page: AppPages) -> some View {
        switch page {
        case .signIn:
            let viewModel = SignInViewModel(authService: services.authService)
            SignInView(viewModel: viewModel)
        // TODO: - Сделать вьюшку + вьюМодель для signUp
        case .signUp:
            let viewModel = SignInViewModel(authService: services.authService)
            SignInView(viewModel: viewModel)
        case .main:
            let viewModel = MainViewModel(
                transactionService: services.transactionService,
                authService: services.authService
            )
            MainView(viewModel: viewModel)
        case .transactions(let username):
            let viewModel = TransactionsViewModel(
                service: services.transactionService,
                username: username
            )
            TransactionsView(viewModel: viewModel)
        }
    }
    
    @ViewBuilder
    func buildCover(cover: FullScreenCover) -> some View {
//        switch cover {
//        case .document: DocumentDetailView()
//        }
    }
    
    @ViewBuilder
    func buildSheet(sheet: Sheet) -> some View {
        switch sheet {
        case .sendFunds(let sender):
            let viewModel = SendFundsViewModel(service: services.transactionService)
            SendFundsView(viewModel: viewModel)
        }
    }
}
