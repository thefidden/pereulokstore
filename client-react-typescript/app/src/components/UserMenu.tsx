import styled from "styled-components";
import { createPortal } from "react-dom";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { HOST, MEDIA } from "../conf.ts";
import { useAppDispatch, useAppSelector } from "../store.ts";
import { authenticateUser, deauthenticateUser } from "../slices/UserSlice.ts";

interface UserMenuProps {
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

    .userData {
        position: absolute;
        bottom: 20px;

        display: grid;
        grid-template-areas: 
                "picture name"
                "picture id";

        grid-template-columns: 1fr 3fr;

        width: 500px;
        height: 100px;
        padding: 5px 10px;

        box-sizing: border-box;
        border: 2px solid transparent;

        color: var(--color-magenta);
        background-color: white;
        border-radius: 100px;

        cursor: pointer;
        user-select: none;
        overflow: hidden;

        font-family: 'Jost', serif;

        transition: transform 0.3s ease-out, box-shadow 0.3s ease-out, border 0.3s ease-out;
        will-change: transform, box-shadow, border;

        &:hover {
            transform: scale(1.05);
            box-shadow: 0 0 30px 15px rgba(205, 92, 92, 1);
            border: 2px solid indianred;

            .deauthenticate {
                opacity: 1;
                filter: blur(0);
            }

            .redLayer {
                opacity: 1;
            }
        }
    }

    .imageFrame {
        display: flex;
        justify-content: center;
        align-items: center;

        grid-area: picture;
        box-sizing: border-box;
        border: 2px solid white;
        border-radius: 100%;

        height: 100%;
        aspect-ratio: 1/1;

        overflow: hidden;

        transition: transform 0.3s ease-out, filter 0.3s ease-out;
        will-change: transform, filter;
    }

    .imageFrame img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .userName {
        grid-area: name;

        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        align-items: flex-start;

        font-size: var(--font-size-regular);

        transition: transform 0.3s ease-out, filter 0.3s ease-out;
        will-change: transform, filter;
    }

    .userId {
        grid-area: id;

        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;

        opacity: 0.5;

        transition: transform 0.3s ease-out, filter 0.3s ease-out;
        will-change: transform, filter;
    }

    .deauthenticate {
        position: absolute;

        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);

        height: 50px;
        padding: 0 30px;

        display: flex;
        align-items: center;
        justify-content: center;

        background-color: red;
        border-radius: 100px;

        font-size: 24px;
        color: white;
        text-wrap: nowrap;

        opacity: 0;
        filter: blur(15px);

        transition: transform 0.3s ease-out, opacity 0.3s ease-out, filter 0.3s ease-out;
        will-change: transform, opacity, filter;
    }

    .redLayer {
        position: absolute;

        background-color: rgba(205, 92, 92, 0.5);
        width: 100%;
        height: 100%;

        opacity: 0;

        transition: transform 0.3s ease-out, opacity 0.3s ease-out;
        will-change: transform, opacity;
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
const LoginButton = styled.div`
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

export default function UserMenu(
    { setMenuOpened }: UserMenuProps
) {
    const navigate = useNavigate()
    const dispatch = useAppDispatch()

    const { user } = useAppSelector(state => state.user)
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
            {
                user === null
                    ? <LoginButton onClick={ () => dispatch(authenticateUser()) }>
                        <div className="title">Войти с помощью Telegram</div>
                    </LoginButton>
                    : <>
                        <div className="pageButton" onClick={ () => navigateTo('/cart') }>
                            <img src={ `${ MEDIA }/cart.jpg` } alt="" />
                            <div className="pageName">Моя корзина</div>
                        </div>

                        <div className="pageButton" onClick={ () => navigateTo('/orders') }>
                            <img src={ `${ MEDIA }/order.jpg` } alt="" />
                            <div className="pageName">Мои заказы</div>
                        </div>

                        <div className="userData" onClick={ () => dispatch(deauthenticateUser()) }>
                            <div className="imageFrame">
                                <img src={ `${ HOST }${ user.image }` } alt="" />
                            </div>
                            <div className="userName">{ user.name }</div>
                            <div className="userId">ID: { user.id }</div>

                            <div className="redLayer"></div>
                            <div className="deauthenticate">Выйти из учетной записи</div>
                        </div>
                    </>
            }

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