const {DataTypes, Model} = require("sequelize");

module.exports = class Record extends Model {
    static init(sequelize, options) {
        super.init({
            id: {
                type: DataTypes.INTEGER,
                primaryKey: true,
                autoIncrement: true,
            },
            players: {
                type: DataTypes.INTEGER,
                defaultValue: 0,
            },
            latency: {
                type: DataTypes.INTEGER,
                defaultValue: 0,
            },
            created_at: {
                type: DataTypes.DATE,
                defaultValue: DataTypes.NOW,
            },
        }, {
            sequelize,
            modelName: 'record',
            tableName: 'records',
            timestamps: false,
        })
    }
};