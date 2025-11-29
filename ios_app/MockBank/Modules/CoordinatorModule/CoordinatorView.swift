import SwiftUI

struct CoordinatorView: View {
    @StateObject private var coordinator = Coordinator()
    var body: some View {
        NavigationStack(path: $coordinator.path) {
            Group {
                if coordinator.isAuthenticated {
                    coordinator.build(page: .main)
                } else {
                    coordinator.build(page: .signIn)
                }
            }
            .navigationDestination(for: AppPages.self) { page in
                coordinator.build(page: page)
            }
            .fullScreenCover(item: $coordinator.fullScreenCover) { item in
                coordinator.buildCover(cover: item)
            }
            .sheet(item: $coordinator.sheet) { item in
                coordinator.buildSheet(sheet: item)
            }
        }
        .environmentObject(coordinator)
    }
}

#Preview {
    CoordinatorView()
}
