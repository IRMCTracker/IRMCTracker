const {DataTypes, Model} = require("sequelize");
const Server = require("./Server");

module.exports = class Vote extends Model {
    static init(sequelize, options) {
        super.init({
            id: {
                type: DataTypes.BIGINT,
                primaryKey: true,
                allowNull: false,
                unique: true,
            },
            username: {
                type: DataTypes.STRING,
                allowNull: false,
            },
            server_id: {
                type: DataTypes.BIGINT,
                allowNull: false,
            },
            created_at: {
                type: DataTypes.DATE,
                allowNull: false,
            },
            updated_at: {
                type: DataTypes.DATE,
                allowNull: false,
            },
        }, {
            sequelize,
            modelName: 'vote',
            tableName: 'votes',
            timestamps: true,
            createdAt: 'created_at',
            updatedAt: 'updated_at',
        });
        Vote.belongsTo(Server, { foreignKey: 'server_id' });
    }
};