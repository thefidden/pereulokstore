import React, { useState } from "react";
import styled from "styled-components";

import { HOSTNAME } from "../conf.js";
import { useNavigate } from "react-router-dom";
import { createPortal } from "react-dom";

export default function NavigationMenu({setNavigationMenuOpened}) {
    const navigate = useNavigate()
    const [closingAnimation, setClosingAnimation] = useState(false)

    const Root = styled.div`
        position: fixed;

        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 20px;

        inset: 0;
        width: 605px;
        height: 100%;

        background-color: #7A89DC;
        z-index: 11;
        box-shadow: 0 0 50px 15px rgba(122, 137, 220, 0.4);

        border-top-right-radius: 100px;
        border-bottom-right-radius: 100px;

        animation: ${closingAnimation ? "fadeOut 0.3s ease-out forwards" : "fadeIn 0.3s ease-out forwards"};

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateX(-5%) scale(1.1);
                filter: blur(30px);
            }
            to {
                opacity: 1;
                transform: translateX(0) scale(1);
                filter: blur(0);
            }
        }

        @keyframes fadeOut {
            from {
                opacity: 1;
                transform: translateX(0) scale(1);
                filter: blur(0);
            }
            to {
                opacity: 0;
                transform: translateX(-5%) scale(1.1);
                filter: blur(30px);
            }
        }

        .pageButton {
            box-sizing: border-box;

            width: 400px;
            height: 190px;

            display: flex;
            align-items: center;
            justify-content: center;

            background-color: white;
            border-radius: 100px;
            border: 2px solid transparent;
            overflow: hidden;

            transition: transform 0.3s ease-out, border 0.3s ease-out, box-shadow 0.3s ease-out;
            will-change: transform, border, box-shadow;

            cursor: pointer;

            &:hover {
                transform: scale(1.05);
                border: 2px solid rgb(177, 217, 225);
                box-shadow: 0 0 30px 15px rgba(177, 217, 225, 0.3);

                img {
                    transform: scale(1.05);
                    filter: brightness(1);
                }
            }

            img {
                width: 100%;
                height: 100%;
                object-fit: cover;

                filter: brightness(0.9);

                transition: transform 0.3s ease-out, filter 0.3s ease-out;
                will-change: transform, filter;
            }
        }

        .pageName {
            position: absolute;

            width: 190px;
            height: 50px;

            display: flex;
            align-items: center;
            justify-content: center;

            background-color: #7A89DC;
            border-radius: 100px;

            font-family: 'Jost', serif;
            font-size: 24px;
            color: white;

            will-change: transform;

            user-select: none;
        }
    `
    const MenuCloseArrow = styled.div`
        position: fixed;

        display: flex;
        justify-content: center;
        align-items: center;

        width: 70px;
        aspect-ratio: 1/1;
        padding: 10px;

        left: 705px;
        top: 50%;
        z-index: 12;

        transform: translateY(-50%);

        opacity: 0;
        background-color: var(--color-magenta);

        box-sizing: border-box;
        border: 2px solid white;
        border-radius: 100%;

        will-change: opacity, transform, filter, box-shadow, left;
        transition: transform 0.3s ease-out, box-shadow 0.3s ease-out;
        animation: arrowFadeIn 0.3s ease-out 0.2s forwards;

        cursor: pointer;

        @keyframes arrowFadeIn {
            from {
                opacity: 0;
                left: 655px;
                filter: blur(10px);
            }
            to {
                opacity: 1;
                left: 705px;
                filter: blur(0);
            }
        }

        &:hover {
            transform: scale(1.1) translateY(-50%);
            box-shadow: 0 0 30px 15px rgba(177, 217, 225, 0.3);
        }
    `
    const Overlay = styled.div`
        position: fixed;

        inset: 0;
        width: 100%;
        height: 100%;

        background-color: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(3px);
        z-index: 10;
        opacity: 0;

        will-change: opacity;
        animation: ${closingAnimation ? "overlayFadeOut 0.15s ease-out forwards" : "overlayFadeIn 0.15s ease-out forwards"};

        @keyframes overlayFadeIn {
            to {
                opacity: 1;
            }
        }

        @keyframes overlayFadeOut {
            from {
                opacity: 1;
            }
            to {
                opacity: 0;
            }
        }
    `

    function closeMenu() {
        setClosingAnimation(true)
        setTimeout(() => setNavigationMenuOpened(false), 300)
    }

    function navigateTo(url) {
        closeMenu()
        navigate(url)
    }

    return (
        <Root>
            <div className = 'pageButton' onClick = {() => navigateTo('/store/?type=comics')}>
                <img id = 'comics-page-image' src = {`${HOSTNAME}/media/static/comics-page.jpg`} alt = ''/>
                <div className = 'pageName'>Комиксы</div>
            </div>

            <div className = 'pageButton' onClick = {() => navigateTo('/store/?type=shape')}>
                <img id = 'shapes-page-image' src = {`${HOSTNAME}/media/static/shapes-page.jpg`} alt = ''/>
                <div className = 'pageName'>Фигурки</div>
            </div>

            <div className = 'pageButton' onClick = {() => navigateTo('/store/?type=suit')}>
                <img id = 'suits-page-image' src = {`${HOSTNAME}/media/static/suits-page.jpg`} alt = ''/>
                <div className = 'pageName'>Костюмы</div>
            </div>

            <MenuCloseArrow onClick = {closeMenu}>
                <svg width = "42" height = "23" viewBox = "0 0 42 23" fill = "none">
                    <path
                        d = "M0.43934 9.98524C-0.146447 10.571 -0.146447 11.5208 0.43934 12.1066L9.98528 21.6525C10.5711 22.2383 11.5208 22.2383 12.1066 21.6525C12.6924 21.0667 12.6924 20.117 12.1066 19.5312L3.62132 11.0459L12.1066 2.56062C12.6924 1.97483 12.6924 1.02508 12.1066 0.439297C11.5208 -0.14649 10.5711 -0.14649 9.98528 0.439297L0.43934 9.98524ZM1.5 11.0459V12.5459H41.5V11.0459V9.5459H1.5V11.0459Z"
                        fill = "white"/>
                </svg>
            </MenuCloseArrow>

            {createPortal(<Overlay onClick = {closeMenu}/>, document.body)}
        </Root>
    )
}