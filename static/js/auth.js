// Authentication utilities for Firebase
export class AuthManager {
    constructor(firebaseConfig) {
        this.app = firebase.initializeApp(firebaseConfig);
        this.auth = firebase.auth();
        this.provider = new firebase.auth.GoogleAuthProvider();
    }

    async signInWithGoogle() {
        try {
            const result = await this.auth.signInWithRedirect(this.provider);
            return result;
        } catch (error) {
            console.error('Sign in error:', error);
            throw error;
        }
    }

    async handleRedirectResult() {
        try {
            const result = await this.auth.getRedirectResult();
            if (result.user) {
                return result.user;
            }
            return null;
        } catch (error) {
            console.error('Redirect result error:', error);
            throw error;
        }
    }

    async signOut() {
        try {
            await this.auth.signOut();
        } catch (error) {
            console.error('Sign out error:', error);
            throw error;
        }
    }

    onAuthStateChanged(callback) {
        return this.auth.onAuthStateChanged(callback);
    }

    async getCurrentUser() {
        return this.auth.currentUser;
    }

    async getIdToken() {
        const user = this.auth.currentUser;
        if (user) {
            return await user.getIdToken();
        }
        return null;
    }
}
