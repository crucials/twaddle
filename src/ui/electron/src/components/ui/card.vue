<script setup lang="ts">
withDefaults(defineProps<{
    heading: string
    tag: string
    lightColorClasses?: string
    /**
     * css classes to apply to card's separate background element,
     * so the gradient color transition can be used
     */
    hoverBackgroundColorClasses?: string
}>(), { tag: "div" })
</script>

<template>
    <Component
        :is="tag"
        class="relative min-h-96 rounded-lg overflow-hidden"
    >
        <div
            v-if="lightColorClasses"
            :class="lightColorClasses"
            class="opacity-40 rounded-full
                w-44 h-44 absolute bottom-0 right-0
                transition-opacity duration-300 blur-2xl"
        >
        </div>

        <div
            class="relative bg-neutral-50/30 border border-neutral-200 rounded-lg
                h-full p-6"
        >
            <div
                v-if="hoverBackgroundColorClasses"
                :class="hoverBackgroundColorClasses"
                class="absolute top-0 left-0
                    w-full h-full rounded-lg
                    transition-opacity duration-300 opacity-0 group-hover:opacity-100"
            >
            </div>

            <h3 class="relative font-medium text-2xl text-neutral-900">
                {{ heading }}
            </h3>

            <slot></slot>
        </div>
    </Component>
</template>
