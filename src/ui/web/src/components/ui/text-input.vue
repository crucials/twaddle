<script setup lang="ts">
withDefaults(defineProps<{
    modelValue: string
    size?: 'small' | 'medium'
    icon?: string
}>(), { size: 'medium' })

const emit = defineEmits<{
    (event: 'update:modelValue', newValue: string): void
}>()
</script>

<template>
    <input
        :value="modelValue"
        type="text"
        class="bg-white rounded-lg text-neutral-800 transition-colors
            flex items-center gap-x-3.5 outline-neutral-800 bg-no-repeat
            border border-neutral-300 hover:border-neutral-400"
        :class="{
            'px-4 py-3.5 sm:px-3 sm:py-3': size === 'medium',
            'px-2.5 py-1.5 sm:px-2': size === 'small'
        }"
        @input="event => emit('update:modelValue', (event.target as HTMLInputElement).value)"
    />
</template>
