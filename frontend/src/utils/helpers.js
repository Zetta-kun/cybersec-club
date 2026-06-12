export const getRankColor = (rating) => {
    if (rating >= 3000) return '#AA0000';
    if (rating >= 2400) return '#FF7777';
    if (rating >= 1900) return '#FF88FF';
    if (rating >= 1600) return '#AAAAFF';
    if (rating >= 1400) return '#77DDBB';
    if (rating >= 1200) return '#77FF77';
    return '#CCCCCC';
};

export const getRankName = (rating) => {
    if (rating >= 3000) return 'Legendary Grandmaster';
    if (rating >= 2400) return 'Grandmaster';
    if (rating >= 1900) return 'Candidate Master';
    if (rating >= 1600) return 'Expert';
    if (rating >= 1400) return 'Specialist';
    if (rating >= 1200) return 'Pupil';
    return 'Newbie';
};
