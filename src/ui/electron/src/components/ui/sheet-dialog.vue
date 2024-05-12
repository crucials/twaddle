<script setup lang="ts">
/**
 * modal visibility can be controlled through v-model or by putting a button
 * into the `triggerButton` slot
*/

import { onKeyStroke } from '@vueuse/core';
import { computed, ref } from 'vue'

const props = withDefaults(defineProps<{
    opened?: boolean
    heading?: string
    triggerButtonContainerClass?: string
}>(), { opened: undefined })

const emit = defineEmits<{
    (event: 'update:opened', newValue: boolean): void
}>()

const openedWithTriggerButton = ref(false)

const modalOpened = computed(() => {
    if(props.opened === undefined) {
        return openedWithTriggerButton.value
    }
    else {
        return props.opened
    }
})

function changeOpenedState(newValue: boolean) {
    if(props.opened === undefined) {
        openedWithTriggerButton.value = newValue
    }
    else {
        emit('update:opened', newValue)
    }
}

onKeyStroke('Escape', () => {
    changeOpenedState(false)
})
</script>

<template>
    <div
        @click="changeOpenedState(true)"
        class="w-fit"
        :class="triggerButtonContainerClass"
    >
        <slot name="triggerButton"></slot>
    </div>

    <Transition enter-from-class="opacity-0" leave-to-class="opacity-0">
        <div
            v-show="modalOpened"
            @mousedown="changeOpenedState(false)"
            class="transition-opacity duration-500 fixed bg-black/40 w-full h-screen top-0 left-0"
        >
        </div>
    </Transition>
    
    <dialog
        class="fixed top-0 right-0 w-1/3 min-w-4.5 max-w-lg h-full mx-0 left-auto bg-white p-6
            block translate-x-full open:translate-x-0 transition-transform duration-500
            sm:min-w-2.5 sm:w-4/5"
        :open="modalOpened"
        v-bind="$attrs"
    >
        <h3 v-if="heading" class="text-2xl font-bold tracking-wide mb-6">
            {{ heading }}
        </h3>
        <slot></slot>

        <button class="absolute top-5 right-4 p-2 rounded-full hover:bg-neutral-100" @click="changeOpenedState(false)">
            <svg class="w-5 h-5" viewBox="-0.5 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 21.32L21 3.32001" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M3 3.32001L21 21.32" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </button>
    </dialog>
</template>
