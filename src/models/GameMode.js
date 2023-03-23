const {DataTypes, Model} = require("sequelize");

module.exports = class GameMode extends Model {
    static init(sequelize, options) {
        super.init({
            id: {
                type: DataTypes.INTEGER,
                primaryKey: true,
                autoIncrement: true,
            },
            name: {
                type: DataTypes.STRING(255),
                unique: true,
            },
        }, {
            sequelize,
            modelName: 'gamemode',
            tableName: 'gamemodes',
            timestamps: false,
        })
    }
};