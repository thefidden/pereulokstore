import { defineStore } from "pinia";

import type { User } from "../interfaces/UserInterface.ts";
import { fetchAuthToken } from "../utils.ts";


export const useUser = defineStore('user', {
    state: () => ({
        user: null as User | null,
        loading: false
    }),
    actions: {
        async fetch() {
            this.loading = true

            try {
                const response: Response = await fetch(`/api/user/`, {
                    method: 'GET',
                    credentials: 'include'
                })

                if (response.status === 204)
                    return

                const { id, username, first_name, image } = await response.json()
                this.user = { id, username, name: first_name, image: image.image }
            }
            catch (e) {
                this.user = null
                console.log('fetchUser error:', e)
            }
            finally {
                this.loading = false
            }
        },

        async authenticate() {
            this.loading = true

            const authToken = await fetchAuthToken()
            const authLink = `https://t.me/pereulokstorebot?start=${authToken}`
            window.open(authLink, '_blank')

            const interval = setInterval(async () => {
                const response = await fetch(`/api/user/authenticate/`, {
                    method: 'post',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        token: authToken
                    })
                })

                if (response.status === 200) {
                    await this.fetch()
                    this.loading = false
                    clearInterval(interval)
                }
            }, 1000)
        },

        async deauthenticate() {
            this.loading = true
            await fetch(`/api/user/deauthenticate/`, {
                method: 'get',
                credentials: 'include'
            })
            this.user = null
            this.loading = false
        }
    }
})