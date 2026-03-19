import React from 'react'
import styled from 'styled-components'
import { HOSTNAME } from "../conf.js";

export default function LoginButton() {
    const Root = styled.div`
        display: flex;
        justify-content: center;
        align-items: center;

        box-sizing: border-box;
        overflow: hidden;

        width: 400px;
        height: 191px;

        border-radius: 100px;
        border: 2px solid white;

        transition: transform 0.3s ease-out, border 0.3s ease-out, box-shadow 0.3s ease-out;
        will-change: transform, border, box-shadow;

        cursor: pointer;

        &:hover {
            transform: scale(1.05);
            border: 2px solid rgb(177, 217, 225);
            box-shadow: 0 0 30px 15px rgba(177, 217, 225, 0.3);
        }

        .title {
            position: absolute;
            
            display: flex;
            justify-content: center;
            align-items: center;

            font-family: 'Jost', serif;
            font-size: var(--font-size-regular);
            font-weight: var(--font-weight-regular);
            color: white;
            text-decoration: none;

            padding: 5px 10px;
            border-radius: 100px;

            background-color: var(--color-magenta);
            user-select: none;

            z-index: 1;
            
            will-change: transform;
        }
        
        img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    `

    async function fetchAuthenticationToken() {
        const response = await fetch(`${HOSTNAME}/api/auth-token/`, {
            method: 'POST'
        })
        const {token} = await response.json()
        return token
    }

    async function buttonClicked() {
        const authenticationToken = await fetchAuthenticationToken()
        const authenticationLink = `https://t.me/pereulokstorebot?start=${authenticationToken}`
        window.open(authenticationLink, '_blank')

        setInterval(async () => {
            const response = await fetch(`${HOSTNAME}/api/user/authenticate/`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    token: authenticationToken
                })
            })

            if (response.status === 200)
                window.location.reload()
        }, 1000)
    }

    return (
        <Root>
            {/*<img src = {`${API_BASE}/media/static/telegram.jpg`}/>*/}
            <div className = 'title' onClick = {buttonClicked}>Войти с помощью Telegram</div>
        </Root>
    )
}