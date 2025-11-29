import Foundation

enum NetworkError: Error {
    case invalidURL
    case noResponse
    case server(Int)
}

class TransactionService {
    private let baseURL: String
    private let session: URLSession
    private let authTokenProvider: () -> String?
    
    init(
        baseURL: String = "https://optimal-sweeping-porpoise.ngrok-free.app/api",
        session: URLSession = .shared,
        authTokenProvider: @escaping () -> String? = { nil }
    ) {
        self.baseURL = baseURL
        self.session = session
        self.authTokenProvider = authTokenProvider
    }
    
    func send(
        requestModel: SendMoneyRequest,
        completion: @escaping (Result<SendMoneyResponse, Error>) -> Void
    ) {
        guard let url = URL(string: baseURL + "/Transaction/Send") else {
            completion(.failure(NetworkError.invalidURL))
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        addDefaultHeaders(to: &request)
        
        request.httpBody = try? JSONEncoder().encode(requestModel)
        
        session.dataTask(with: request) {data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let http = response as? HTTPURLResponse, let data = data else {
                completion(.failure(NetworkError.noResponse))
                return
            }
            
            if (200...299).contains(http.statusCode) {
                do {
                    let responseObj = try JSONDecoder().decode(SendMoneyResponse.self, from: data)
                    completion(.success(responseObj))
                    
                } catch {
                    print("Decode error: \(error)")
                    completion(.failure(error))
                }
            } else {
                completion(.failure(NetworkError.server(http.statusCode)))
            }
        }.resume()
    }
    
    func getAll(
        completion: @escaping (Result<[Transaction], Error>) -> Void
    ) {
        print("DEGUB URL: '\(baseURL + "/Transaction/GetAll")'")
        guard let url = URL(string: baseURL + "/Transaction/GetAll") else {
            completion(.failure(NetworkError.invalidURL))
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        addDefaultHeaders(to: &request)
        
        session.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let data = data else { completion(.failure(NetworkError.noResponse)); return }
            
            do {
                let dtos = try JSONDecoder().decode([TransactionResponse].self, from: data)
                
                let domainModels = dtos.map { Transaction(from: $0) }
                
                completion(.success(domainModels))
            } catch {
                print("Decoding Error: \(error)")
                completion(.failure(error))
            }
        }.resume()
    }
}

extension TransactionService {
    
}

private extension TransactionService {
    func addDefaultHeaders(to request: inout URLRequest) {
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let token = authTokenProvider() {
            request.addValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }
    }
}
