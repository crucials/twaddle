<script setup lang="ts">
import SelectField from '@/components/ui/select-input.vue'
import { ref } from 'vue'

const wordLists = [
    'all', 'english swears', 'english swears1', 'english2', 'english54343', '12312', '125467', '000'
].map(label => ({
    name: label, 
    label: label
}))

const selectedWordList = ref('all')
</script>

<template>
    <form
        class="bg-neutral-100 rounded-lg max-w-[1080px] px-8 py-7
            flex items-start gap-x-14 h-72"
        @submit.prevent=""
    >
        <button
            class="w-28 h-28 bg-white shadow-black/30 shadow-2xl rounded-full
                flex items-center justify-center
                transition-transform duration-300 hover:scale-105"
            title="start words counter"
        >
            <svg class="w-8" viewBox="0 0 33 44" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                    d="M8.5 8C8.5 3.58172 12.0817 0 16.5 0C20.9182 0 24.5 3.58172 24.5 8V22C24.5 26.4182 20.9182 30 16.5 30C12.0817 30 8.5 26.4182 8.5 22V8Z"
                    fill="#F75757" />
                <path
                    d="M5 21.6876V22C5 25.05 6.2116 27.975 8.36828 30.1318C10.5249 32.2884 13.45 33.5 16.5 33.5C19.55 33.5 22.475 32.2884 24.6318 30.1318C26.7884 27.975 28 25.05 28 22V21.6876C28 20.583 28.8954 19.6876 30 19.6876H31C32.1046 19.6876 33 20.583 33 21.6874V22C33 26.376 31.2616 30.573 28.1672 33.6672C25.6684 36.1662 22.4506 37.7806 19 38.3096V42C19 43.1046 18.1046 44 17 44H16C14.8954 44 14 43.1046 14 42V38.3096C10.5494 37.7806 7.33158 36.1662 4.83274 33.6672C1.73838 30.573 0 26.376 0 22V21.6876C0 20.583 0.89544 19.6876 2 19.6876H3C4.10456 19.6876 5 20.583 5 21.6876Z"
                    fill="#F75757" />
            </svg>
        </button>
        
        <label>
            <div class="mb-1">
                words to count
            </div>
            <SelectField
                :items="wordLists"
                v-model:selectedItemName="selectedWordList"
                placeholder="select the word list"
            />
        </label>
    </form>
</template>
