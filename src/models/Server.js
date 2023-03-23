const {DataTypes, Model} = require("sequelize");

module.exports = class Server extends Model {
    static init(sequelize, options) {
        super.init({
            id: {
                type: DataTypes.INTEGER,
                primaryKey: true,
                autoIncrement: true,
            },
            name: {
                type: DataTypes.STRING(150),
                unique: true,
            },
            description: {
                type: DataTypes.TEXT('long'),
                allowNull: true,
            },
            address: {
                type: DataTypes.STRING(150),
                unique: true,
            },
            ip: {
                type: DataTypes.STRING(150),
                allowNull: true,
            },
            country_code: {
                type: DataTypes.STRING(50),
                allowNull: true,
            },
            region: {
                type: DataTypes.STRING(100),
                allowNull: true,
            },
            favicon_path: {
                type: DataTypes.TEXT,
                allowNull: true,
            },
            info_path: {
                type: DataTypes.TEXT,
                allowNull: true,
            },
            motd_path: {
                type: DataTypes.TEXT,
                allowNull: true,
            },
            gamemodes: {
                type: DataTypes.TEXT,
                allowNull: true,
            },
            latest_version: {
                type: DataTypes.STRING(255),
                allowNull: true,
            },
            latest_latency: {
                type: DataTypes.INTEGER,
                allowNull: true,
                defaultValue: 0,
            },
            current_players: {
                type: DataTypes.INTEGER,
                allowNull: true,
                defaultValue: 0,
            },
            max_players: {
                type: DataTypes.INTEGER,
                allowNull: true,
                defaultValue: 0,
            },
            up_from: {
                type: DataTypes.BIGINT,
                allowNull: false,
                defaultValue: 0,
            },
            is_vip: {
                type: DataTypes.BOOLEAN,
                allowNull: false,
                defaultValue: false,
            },
            channel_id: {
                type: DataTypes.BIGINT,
                allowNull: false,
                defaultValue: 0,
            },
            is_active: {
                type: DataTypes.BOOLEAN,
                allowNull: false,
                defaultValue: true,
            },
        }, {
            sequelize,
            modelName: 'server',
            timestamps: false,
        })
    }
};