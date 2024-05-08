<script setup lang="ts">
import Card from '@/components/ui/card.vue'
</script>

<template>
    <nav
        class="grid grid-cols-[repeat(auto-fit,minmax(100px,320px))] gap-14"
    >
        <Card
            heading="record and analyze"
            tag="RouterLink"
            to="/record"
            light-color-classes="bg-red-400"
            hover-background-color-classes="bg-gradient-to-r from-red-400 to-rose-200"
            class="group"
        >
            <img
                src="@/assets/images/microphone-illustration.png"
                alt="microphone illustration"
                class="absolute -bottom-10 -left-10 w-48
                    transition-transform duration-300 group-hover:scale-110"
            />
        </Card>

        <Card
            heading="transcribe from file"
            tag="RouterLink"
            to="/transcribe-from-file"
            light-color-classes="bg-purple-500"
            hover-background-color-classes="bg-gradient-to-r from-purple-500 to-violet-200"
            class="group"
        >
            <img
                src="@/assets/images/music-note-illustration.png"
                alt="music note illustration"
                class="absolute -bottom-4 -left-4 w-44
                    transition-transform duration-300 group-hover:scale-110"
            />
        </Card>
    </nav>
</template>
