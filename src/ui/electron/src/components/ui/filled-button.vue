<script setup lang="ts">
import { ref } from 'vue'
import { useElementSize } from '@vueuse/core'

defineProps<{
    tag?: string
}>()

const buttonElement = ref<HTMLButtonElement>()
const buttonSize = useElementSize(buttonElement, undefined, { box: 'border-box' })
</script>

<template>
    <Component
        :is="tag || 'button'"
        ref="buttonElement"
        class="filled-button bg-neutral-800 rounded-lg px-7 py-2.5
            relative overflow-hidden"
    >
        <div class="polygon-background-container">
            <div
                class="polygon-background"
                :style="{ height: `${buttonSize.height.value}px` }"
            ></div>
        </div>
        <span class="relative text-white flex items-center gap-x-2">
            <slot></slot>
        </span>
    </Component>    
</template>

<style scoped>
.polygon-background-container {
    @apply absolute top-0 left-0 w-full h-0 overflow-hidden transition-all duration-300;
}

.polygon-background {
    clip-path: polygon(0 0, 50% 0, 100% 100%, 50% 100%);
    background-color: rgb(255 255 255 / 0.055);
    @apply w-full;
}

.filled-button:hover .polygon-background-container {
    @apply h-full;
}
</style>
