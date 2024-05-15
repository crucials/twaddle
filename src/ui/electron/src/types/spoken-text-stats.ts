export type WordStats = {
    word: string
    count: number
}

export interface SpokenTextStats {
    wordsStats: WordStats[]
    fullText: string
}
