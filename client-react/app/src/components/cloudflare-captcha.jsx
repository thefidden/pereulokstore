import React, { useEffect, useRef } from "react";
import styled from "styled-components";

import { CLOUDFLARE_SITE_KEY } from "../conf.js";

const CloudflareCaptcha = ({onVerify}) => {
    const ref = useRef(null)

    useEffect(() => {
        if (!window.turnstile) return

        window.turnstile.render(ref.current, {
            sitekey: SITE_KEY,
            callback: function (token) {
                onVerify(token)
            }
        })
    }, [])

    return <div ref = {ref}></div>
}

export default CloudflareCaptcha