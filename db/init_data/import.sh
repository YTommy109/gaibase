#/bin/sh

# アカウント
psql -d gaibase_dev -U tokutomi -c "\copy accounts(id,email,name,role) from db/init_data/accounts.csv delimiter ',' csv header;"

# ワークスペース
psql -d gaibase_dev -U tokutomi -c "\copy workspaces(id,title) from db/init_data/workspaces.csv delimiter ',' csv header;"

# ワークスペースメンバー
psql -d gaibase_dev -U tokutomi -c "\copy workspace_members(account_id,workspace_id,role) from db/init_data/workspace_members.csv delimiter ',' csv header;"
