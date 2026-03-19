import styled from 'styled-components'
import { HOSTNAME } from "../conf.js";
import {deauthenticate} from "../utils.js";

export default function LogoutButton() {
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

        &::before {
            content: '';
            position: absolute;
            inset: 0;

            background-color: white;
            background-image: url('${HOSTNAME + '/media/static/telegram.svg'}');
            background-repeat: space;
            background-size: 60px 30px;

            transition: transform 0.3s ease-out;
            will-change: transform;
        }

        &:hover::before {
            transform: scale(1.05);
        }

        .title {
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
        }
    `

    return (
        <Root>
            <div className = 'title' onClick = {deauthenticate}>Выйти из учетной записи</div>
        </Root>
    )
}