"""Ajout des colonnes manquantes à diagnostic_reponses"""

from alembic import op
import sqlalchemy as sa


# Révisions Alembic
revision = "20250921_add_diag_columns"
down_revision = None   # ⚠️ Mets l’ID de la dernière migration si tu en as déjà une
branch_labels = None
depends_on = None


def upgrade():
    # Ajout des colonnes si elles n'existent pas déjà
    with op.batch_alter_table("diagnostic_reponses") as batch_op:
        batch_op.add_column(sa.Column("nom_scientifique", sa.String(255)))
        batch_op.add_column(sa.Column("origine", sa.String(255)))
        batch_op.add_column(sa.Column("sol", sa.String(255)))
        batch_op.add_column(sa.Column("varietes", sa.JSON))
        batch_op.add_column(sa.Column("rendement", sa.String(255)))
        batch_op.add_column(sa.Column("nutrition", sa.JSON))
        batch_op.add_column(sa.Column("toxicite", sa.String(1000)))
        batch_op.add_column(sa.Column("medicinal", sa.String(1000)))
        batch_op.add_column(sa.Column("produits", sa.JSON))
        batch_op.add_column(sa.Column("saisons", sa.String(255)))
        batch_op.add_column(sa.Column("itineraire", sa.String(2000)))


def downgrade():
    # Suppression si rollback
    with op.batch_alter_table("diagnostic_reponses") as batch_op:
        batch_op.drop_column("nom_scientifique")
        batch_op.drop_column("origine")
        batch_op.drop_column("sol")
        batch_op.drop_column("varietes")
        batch_op.drop_column("rendement")
        batch_op.drop_column("nutrition")
        batch_op.drop_column("toxicite")
        batch_op.drop_column("medicinal")
        batch_op.drop_column("produits")
        batch_op.drop_column("saisons")
        batch_op.drop_column("itineraire")
