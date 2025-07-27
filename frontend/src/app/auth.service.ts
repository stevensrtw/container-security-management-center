import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private tokenKey = 'jwt_token';

  loginWithMockOIDC(username: string, role: string): void {
    // Simulate OIDC token and user
    const fakeToken = btoa(`${username}.${role}.${Date.now()}`);
    localStorage.setItem(this.tokenKey, fakeToken);
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}