import { API } from "./conf.ts";

export function getCookie(name: string) {
    let cookieValue = null

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break
            }
        }
    }

    return cookieValue
}

export async function fetchAuthToken() {
    try {
        const response = await fetch(`${API}/auth-token/`, {
            method: 'POST'
        })
        const { token } = await response.json()
        return token
    }
    catch (e) {
        console.log('fetchAuthToken error:', e)
    }
}