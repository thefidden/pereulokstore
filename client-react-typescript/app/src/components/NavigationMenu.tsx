import styled from "styled-components";
import { createPortal } from "react-dom";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { MEDIA } from "../conf.ts";

interface NavigationMenuProps {
    setMenuOpened(value: boolean): void
}

interface RootProps {
    closingAnimation: boolean
}

interface OverlayProps {
    closingAnimation: boolean
}

const Root = styled.div<RootProps>`
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

    animation: ${ props =>
            !props.closingAnimation
                    ? "fadeIn 0.3s ease-out forwards"
                    : "fadeOut 0.3s ease-out forwards"
    };

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
        }

        &:hover img {
            transform: scale(1.05);
            filter: brightness(1);
        }
    }

    .pageButton img {
        width: 100%;
        height: 100%;
        object-fit: cover;

        filter: brightness(0.9);

        transition: transform 0.3s ease-out, filter 0.3s ease-out;
        will-change: transform, filter;
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

    &:hover {
        transform: translateY(-50%) scale(1.1);
        box-shadow: 0 0 30px 15px rgba(177, 217, 225, 0.3);
    }

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
`
const Overlay = styled.div<OverlayProps>`
    position: fixed;

    inset: 0;
    width: 100%;
    height: 100%;

    background-color: rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(3px);
    z-index: 10;
    opacity: 0;

    will-change: opacity;
    animation: ${ props =>
            !props.closingAnimation
                    ? "overlayFadeIn 0.15s ease-out forwards"
                    : "overlayFadeOut 0.15s ease-out forwards"
    };

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

export default function NavigationMenu(
    { setMenuOpened }: NavigationMenuProps
) {
    const navigate = useNavigate()
    const [closingAnimation, setClosingAnimation] = useState<boolean>(false)

    function closeMenu() {
        setClosingAnimation(true)
        setTimeout(() => setMenuOpened(false), 300)
    }

    function navigateTo(to: string) {
        closeMenu()
        navigate(to)
    }

    return (
        <Root closingAnimation={ closingAnimation }>
            <div className="pageButton" onClick={ () => navigateTo('/store/?type=comics') }>
                <img id="comics-page-image" src={ `${ MEDIA }/comics-page.jpg` } alt="" />
                <div className="pageName">Комиксы</div>
            </div>

            <div className="pageButton" onClick={ () => navigateTo('/store/?type=shape') }>
                <img id="shapes-page-image" src={ `${ MEDIA }/shapes-page.jpg` } alt="" />
                <div className="pageName">Фигурки</div>
            </div>

            <div className="pageButton" onClick={ () => navigateTo('/store/?type=suit') }>
                <img id="suits-page-image" src={ `${ MEDIA }/suits-page.jpg` } alt="" />
                <div className="pageName">Костюмы</div>
            </div>

            <MenuCloseArrow onClick={ closeMenu }>
                <svg width="42" height="23" viewBox="0 0 42 23" fill="none">
                    <path
                        d="M0.43934 9.98524C-0.146447 10.571 -0.146447 11.5208 0.43934 12.1066L9.98528 21.6525C10.5711 22.2383 11.5208 22.2383 12.1066 21.6525C12.6924 21.0667 12.6924 20.117 12.1066 19.5312L3.62132 11.0459L12.1066 2.56062C12.6924 1.97483 12.6924 1.02508 12.1066 0.439297C11.5208 -0.14649 10.5711 -0.14649 9.98528 0.439297L0.43934 9.98524ZM1.5 11.0459V12.5459H41.5V11.0459V9.5459H1.5V11.0459Z"
                        fill="white" />
                </svg>
            </MenuCloseArrow>

            {
                createPortal(
                    <Overlay closingAnimation={ closingAnimation } onClick={ closeMenu } />,
                    document.body
                )
            }
        </Root>
    )
}