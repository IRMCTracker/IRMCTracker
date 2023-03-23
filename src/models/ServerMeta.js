const {DataTypes, Model} = require("sequelize");
const Server = require('./Server');

module.exports = class ServerMeta extends Model {
    static init(sequelize, options) {
        super.init({
            key: {
                type: DataTypes.STRING(255),
                allowNull: false,
            },
            value: {
                type: DataTypes.TEXT('long'),
                allowNull: false,
            },
        }, {
            sequelize,
            modelName: 'server_meta',
            tableName: 'servers_meta',
            timestamps: false,
            indexes: [
                { unique: true, fields: ['key', 'server_id'] },
            ],
        })
        ServerMeta.belongsTo(Server, { foreignKey: 'server_id' });
    }
};