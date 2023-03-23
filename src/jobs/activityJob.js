const activities = [
    "💎 Visit MCTracker.iR",
    "🤌🏻 You can vote to servers on our site!"
];

module.exports = {
    interval: 5000,
    execute: async () => {
        const newActivity = activities[Math.floor(Math.random() * activities.length)];

        client.user.setActivity(newActivity);
    }
}
