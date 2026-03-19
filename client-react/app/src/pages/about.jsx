import React from "react";
import styled from 'styled-components'

import { HOSTNAME } from "../conf.js";
import Header from "../components/header.jsx";

export default function AboutPage() {
    const Root = styled.div`
        max-width: 1440px;
        margin: 0 auto;

        display: flex;
        flex-direction: column;
        gap: 100px;

        font-family: 'Jost', serif;

        .info {
            position: relative;

            display: flex;
            flex-direction: row;
            gap: 20px;

            width: 100%;
        }

        .addressColumn, .contactsColumn {
            flex: 1;

            display: flex;
            flex-direction: column;
            gap: 20px;

            align-items: flex-start;
        }

        .addressTitle, .contactsTitle {
            display: flex;
            justify-content: center;
            align-items: center;

            width: 60%;
            height: 100px;

            background-color: white;
            border-radius: 100px;

            color: var(--color-magenta);
            font-size: 48px;
            font-weight: var(--font-weight-bold);

            user-select: none;
        }

        .address, .contact {
            display: flex;
            justify-content: center;
            align-items: center;

            width: 100%;
            height: 50px;

            background-color: white;
            border-radius: 100px;

            color: black;
            font-size: 24px;
            font-weight: var(--font-weight-regular);
        }

        .imageFrame {
            width: 100%;
            height: 400px;
            border-radius: 100px;
            overflow: hidden;
            
            background-color: white;

            img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
        }
    `

    return (
        <Root>
            <Header></Header>

            <div className = 'info'>
                <div className = 'addressColumn'>
                    <div className = 'imageFrame'>
                        <img src = {`${HOSTNAME}/media/static/map.jpg`}/>
                    </div>

                    <div className = 'addressTitle'>Адрес</div>
                    <div className = 'address'>Варшавское шоссе, 16к1, Москва, 117105</div>
                </div>

                <div className = 'contactsColumn'>
                    <div className = 'imageFrame'>
                        <img src = {`${HOSTNAME}/media/static/phone.jpg`}/>
                    </div>

                    <div className = 'contactsTitle'>Контакты</div>
                    <div className = 'contact'>+7 (965) 281-00-79</div>
                </div>
            </div>
        </Root>
    )
}