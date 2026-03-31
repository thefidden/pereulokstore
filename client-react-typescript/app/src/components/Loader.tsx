import React from "react";
import styled from "styled-components";
import { createPortal } from "react-dom";

const Root = styled.div`
    position: fixed;

    display: flex;
    align-items: center;
    justify-content: center;

    inset: 0;
    width: 100%;
    height: 100%;

    background-color: rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(3px);
    opacity: 1;
`

const LoadingAnimation = styled.div`
    width: 70px;
    height: 70px;

    border-radius: 50%;
    background: var(--color-magenta);

    animation: pulse 1.2s ease-in-out infinite;

    @keyframes pulse {
        0% {
            transform: scale(0.8);
            opacity: 0.5;
            filter: blur(10px);
        }
        50% {
            transform: scale(1.2);
            opacity: 1;
            filter: blur(0);
        }
        100% {
            transform: scale(0.8);
            opacity: 0.5;
            filter: blur(10px);
        }
    }
`

export default function Loader() {
    return createPortal(
        <Root><LoadingAnimation /></Root>,
        document.body
    )
}
