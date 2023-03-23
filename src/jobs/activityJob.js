const activities = [
    "💎 Visit MCTracker.iR",
    "🤌🏻 You can vote to servers on our site!"
];

/**
 * Changing activity every x seconds
 * 
 * TODO showing dynamic activities such as servers count, etc
 */
module.exports = {
    interval: 5000,
    async execute() {
        const newActivity = activities[Math.floor(Math.random() * activities.length)];

        client.user.setActivity(newActivity);
    }
}
