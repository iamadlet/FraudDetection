import Foundation

final class AuthService {
    private let baseURL: String
    private let session: URLSession
    private let tokenKey = "token"
    
    init(baseURL: String = "https://optimal-sweeping-porpoise.ngrok-free.app/api", session: URLSession = .shared) {
        self.baseURL = baseURL
        self.session = session
    }
}

extension AuthService {
    func signIn(
        request: SignInRequest,
        completion: @escaping (Result<AuthResponse, Error>) -> Void
    ) {
        guard let url = URL(string: baseURL + "/User/SignIn") else {
            completion(.failure(AuthError.invalidURL))
            return
        }
        
        var req = URLRequest(url: url)
        req.httpMethod = "POST"
        req.addValue("application/json", forHTTPHeaderField: "Content-Type")
        req.httpBody = try? JSONEncoder().encode(request)
        
        session.dataTask(with: req) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let http = response as? HTTPURLResponse, let data = data else {
                completion(.failure(AuthError.noResponse))
                return
            }
            
            if (200...299).contains(http.statusCode) {
                do {
                    let auth = try JSONDecoder().decode(AuthResponse.self, from: data)
                    
                    try? KeychainManager.instance.saveToken(auth.token, forKey: self.tokenKey)
                    completion(.success(auth))
                } catch {
                    completion(.failure(error))
                }
            } else {
                completion(.failure(AuthError.server(http.statusCode)))
            }
        }.resume()
    }
    
    func signUp(
        request: SignInRequest,
        completion: @escaping (Result<AuthResponse, Error>) -> Void
    ) {
        guard let url = URL(string: baseURL + "/User/SignUp") else {
            completion(.failure(AuthError.invalidURL))
            return
        }
        
        var req = URLRequest(url: url)
        req.httpMethod = "POST"
        req.addValue("application/json", forHTTPHeaderField: "Content-Type")
        req.httpBody = try? JSONEncoder().encode(request)
        
        session.dataTask(with: req) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let http = response as? HTTPURLResponse, let data = data else {
                completion(.failure(AuthError.noResponse))
                return
            }
            
            if (200...299).contains(http.statusCode) {
                do {
                    let auth = try JSONDecoder().decode(AuthResponse.self, from: data)
                    
                    try? KeychainManager.instance.saveToken(auth.token, forKey: self.tokenKey)
                    
                    completion(.success(auth))
                } catch {
                    completion(.failure(error))
                }
            } else {
                completion(.failure(AuthError.server(http.statusCode)))
            }
        }.resume()
    }
    
    func getCurrentUser(completion: @escaping (Result<UserProfileResponse, Error>) -> Void) {
        guard let url = URL(string: baseURL + "/User/GetCurrentUser") else {
            completion(.failure(AuthError.invalidURL))
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let token = getSavedToken() {
            request.addValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }
        
        session.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let http = response as? HTTPURLResponse, (200...299).contains(http.statusCode), let data = data else {
                completion(.failure(AuthError.noResponse))
                return
            }
            
            do {
                let user = try JSONDecoder().decode(UserProfileResponse.self, from: data)
                completion(.success(user))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }
    
    func logout() {
        KeychainManager.instance.deleteToken(forKey: tokenKey)
    }
    
    func getSavedToken() -> String? {
        KeychainManager.instance.getToken(forKey: tokenKey)
    }
}
