import { createSlice, createAsyncThunk } from "@reduxjs/toolkit"
import type { User } from "../interfaces/UserInterface.ts";
import { API } from "../conf.ts";
import { fetchAuthToken } from "../utils.ts";

interface State {
    user: User | null,
    loading: boolean
}

export const fetchUser = createAsyncThunk(
    "user/fetch",
    async (): Promise<User | null> => {
        const response = await fetch(`${API}/user/`, {
            method: "GET",
            credentials: "include"
        })

        if (response.status === 204)
            return null

        const { id, username, first_name: name, image } = await response.json()

        return {
            id: id,
            username: username,
            name: name,
            image: image.image
        } as User
    }
)

export const authenticateUser = createAsyncThunk(
    "user/authenticate",
    async (_, { dispatch }) => {
        const authToken = await fetchAuthToken()
        const authLink = `https://t.me/pereulokstorebot?start=${authToken}`
        window.open(authLink, "_blank")

        return new Promise<void>((resolve) => {
            const interval = setInterval(async () => {
                const response = await fetch(`${API}/user/authenticate/`, {
                    method: "post",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        token: authToken
                    })
                })

                if (response.status === 200) {
                    await dispatch(fetchUser())
                    clearInterval(interval)
                    resolve()
                }
            })
        })
    }
)

export const deauthenticateUser = createAsyncThunk(
    "user/deauthenticate",
    async () => {
        await fetch(`${API}/user/deauthenticate`, {
            method: "get",
            credentials: "include"
        })
    }
)

export const UserSlice = createSlice({
    name: "user",

    initialState: {
        user: null,
        loading: false
    } as State,

    reducers: {},

    extraReducers: (builder) => {
        builder
            .addCase(fetchUser.pending, (state) => {
                state.loading = true
            })
            .addCase(fetchUser.fulfilled, (state, action) => {
                state.user = action.payload
                state.loading = false
            })
            .addCase(fetchUser.rejected, (state) => {
                console.log("fetchUser error")
                state.user = null
                state.loading = false
            })

            .addCase(authenticateUser.pending, (state) => {
                state.loading = true
            })
            .addCase(authenticateUser.fulfilled, (state) => {
                state.loading = false
            })
            .addCase(authenticateUser.rejected, (state) => {
                state.loading = false
            })

            .addCase(deauthenticateUser.pending, (state) => {
                state.loading = true
            })
            .addCase(deauthenticateUser.fulfilled, (state) => {
                state.user = null
                state.loading = false
            })
            .addCase(deauthenticateUser.rejected, (state) => {
                state.loading = false
            })
    }
})

export const userReducer = UserSlice.reducer