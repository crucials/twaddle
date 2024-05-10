<script setup lang="ts">
import { ref } from 'vue'
import { useDropZone } from '@vueuse/core'

defineProps<{
    modelValue: File | null
    accept?: string
}>()
const emit = defineEmits<{
    (event : 'update:modelValue', file : File) : void
}>()

const fileInputElement = ref<HTMLInputElement>()
const uploadArea = ref<HTMLSpanElement>()

const { isOverDropZone } = useDropZone(uploadArea, {
    onDrop(files) {
        if(files && files.length > 0) {
            emit('update:modelValue', files[0])
        }
    }
})

function updateFile() {
    const files = fileInputElement.value?.files

    console.log(files)

    if(files && files.length > 0) {
        emit('update:modelValue', files[0])
    }
}
</script>

<template>
    <label>
        <slot></slot>
        
        <div
            ref="uploadArea"
            role="button"
            class="p-7 border-2 rounded-lg
                flex items-center gap-x-4 text-base group
                transition-colors duration-300
                focus:border-neutral-800 focus:outline-none lg:p-6 sm:p-4"
            :class="{
                'border-solid border-neutral-600': isOverDropZone,
                'border-dashed border-neutral-300': !isOverDropZone
            }"
            aria-controls="filename"
            tabindex="0"
        >
            <svg
                width="36" height="36"
                viewBox="0 0 30 30"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                class="transition-transform duration-300 group-hover:scale-110 flex-shrink-0"
            >
                <rect width="30" height="30" rx="15" fill="black"/>
                <path d="M20.2621 20.2344H20.2723M18.8359 17.1803H21.2808C22.2302 17.1803 22.7048 17.1803 23.0793 17.3353C23.5785 17.5419 23.9752 17.9384 24.182 18.4372C24.337 18.8114 24.337 19.2857 24.337 20.2344C24.337 21.1831 24.337 21.6575 24.182 22.0317C23.9752 22.5305 23.5785 22.9269 23.0793 23.1336C22.7048 23.2885 22.2302 23.2885 21.2808 23.2885H9.05617C8.10684 23.2885 7.63218 23.2885 7.25775 23.1336C6.75852 22.9269 6.36188 22.5305 6.15509 22.0317C6 21.6575 6 21.1831 6 20.2344C6 19.2857 6 18.8114 6.15509 18.4372C6.36188 17.9384 6.75852 17.5419 7.25775 17.3353C7.63218 17.1803 8.10684 17.1803 9.05617 17.1803H11.5011M15.1685 18.1984V7M15.1685 7L18.2247 10.0541M15.1685 7L12.1123 10.0541" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>

            <p class="text-neutral-600" v-if="modelValue === null">
                upload a file (<span class="text-neutral-800 font-medium">click</span>
                or <span class="text-neutral-800 font-medium">drag and drop</span>)
            </p>

            <p v-else class="max-w-80 line-clamp-2">
                {{ modelValue.name }}
            </p>
        </div>

        <input
            ref="fileInputElement"
            type="file"
            class="hidden"
            @input="updateFile"
            :accept="accept"
        />
    </label>
</template>
