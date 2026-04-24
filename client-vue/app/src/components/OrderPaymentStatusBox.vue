<script setup lang="ts">
    import { computed, ref } from "vue";

    const emits = defineEmits(["close"])

    const { orderId, paymentStatus } = defineProps<{
        orderId: string,
        paymentStatus: "successful" | "failure"
    }>()

    const closingAnimation = ref(false)

    const paymentStatusTranslated = computed(() =>
        paymentStatus === "successful"
        ? "Заказ успешно создан"
        : "Ошибка создания заказа"
    )

    function close () {
        closingAnimation.value = true
        setTimeout(() => emits('close'), 300)
    }
</script>

<template>
    <Teleport to="body">
        <div :class="['root', !closingAnimation ? 'fadeIn' : 'fadeOut']">
            <div :class="['box', paymentStatus, 'fadeIn']">
                <div class="title">Заказ {{ orderId.toUpperCase() }}</div>
                <div class="description">{{ paymentStatusTranslated }}</div>
                <div class="closeButton" @click="close">ОК</div>
            </div>
        </div>
    </Teleport>
</template>

<style scoped>
    .root {
        position: fixed;

        display: flex;
        align-items: center;
        justify-content: center;

        inset: 0;
        width: 100%;
        height: 100%;
        z-index: 20;

        background-color: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(3px);
        opacity: 0;

        will-change: opacity, transform, filter;
    }

    .box {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        z-index: 22;

        box-sizing: border-box;
        padding: 100px 200px;
        gap: 50px;

        background-color: white;
        border-radius: 100px;

        font-family: 'Jost', serif;
        text-wrap: nowrap;

        opacity: 0;
        user-select: none;

        will-change: opacity, transform, filter;
    }

    .title {
        font-size: 48px;
        font-weight: var(--font-weight-bold);
    }

    .description {
        font-size: 32px;
    }

    .closeButton {
        position: absolute;

        z-index: 21;

        display: flex;
        justify-content: center;
        align-items: center;

        box-sizing: border-box;
        padding: 20px 50px;

        background-color: var(--color-magenta);
        border-radius: 100px;

        font-family: 'Jost', serif;
        font-size: 32px;
        font-weight: var(--font-weight-bold);
        color: white;

        user-select: none;
        cursor: pointer;
        opacity: 0;

        will-change: transform, box-shadow, opacity, filter;
        transition: transform 0.3s ease-out, box-shadow 0.3s ease-out;
        animation: CloseButtonSlideIn 0.3s ease-out 0.3s forwards;

        &:hover {
            transform: scale(1.05);
            box-shadow: 0 0 30px 15px rgba(122, 137, 220, 0.3);
        }
    }

    .box.successful { box-shadow: 0 0 50px 15px rgba(46, 158, 111, 0.5); }
    .box.failure { box-shadow: 0 0 50px 15px rgba(214, 69, 80, 0.5) }

    .box.successful .title,
    .box.successful .description { color: var(--color-green) }

    .box.failure .title,
    .box.failure .description { color: var(--color-red) }

    .box.fadeIn { animation: BoxFadeIn 0.3s ease-out forwards }
    .root.fadeIn { animation: OrderPaymentStatusRootFadeIn 0.3s ease-out forwards }
    .root.fadeOut { animation: OrderPaymentStatusRootFadeOut 0.2s ease-out forwards }

    @keyframes BoxFadeIn {
        from {
            opacity: 0;
            transform: scale(1.2);
            filter: blur(30px);
        }
        to {
            opacity: 1;
            transform: scale(1);
            filter: blur(0);
        }
    }

    @keyframes CloseButtonSlideIn {
        from {
            opacity: 0;
            bottom: -100px;
            filter: blur(30px);
        }
        to {
            opacity: 1;
            bottom: -150px;
            filter: blur(0);
        }
    }

    @keyframes OrderPaymentStatusRootFadeIn {
        to {
            opacity: 1;
        }
    }

    @keyframes OrderPaymentStatusRootFadeOut {
        from {
            opacity: 1;
            transform: scale(1);
            filter: blur(0);
        }
        to {
            opacity: 0;
            transform: scale(1.2);
            filter: blur(30px);
        }
    }
</style>