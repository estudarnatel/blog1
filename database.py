# from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from sqlalchemy import create_engine, text, Table, MetaData, select, func
from config import DATABASE_CONFIG
from typing import Optional
from sqlalchemy import cast, Float
import pandas as pd


DATABASE_URL = (
    f"mssql+pymssql://{DATABASE_CONFIG['username']}:"
    f"{DATABASE_CONFIG['password']}@"
    f"{DATABASE_CONFIG['server']}/"
    f"{DATABASE_CONFIG['database']}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

metadata = MetaData()

# =========================
# aprovados CSV
# =========================
def insert_aprovados(lista_resultados, table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        with engine.begin() as conn:
            conn.execute(table.insert(), lista_resultados)

        return True

    except SQLAlchemyError as e:
        print(f"Erro ao inserir aprovados: {str(e)}")
        return False


def get_aprovados(table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = select(table)

        with engine.connect() as conn:
            result = conn.execute(stmt)
            return result.fetchall()

    except SQLAlchemyError as e:
        print(f"Erro ao buscar aprovados: {str(e)}")
        return []
    

def get_aprovados_by_nome(nome, table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = select(table).where(table.c.Nome.ilike(f"%{nome}%"))

        with engine.connect() as conn:
            result = conn.execute(stmt)
            return result.fetchall()

    except SQLAlchemyError as e:
        print(f"Erro ao buscar aprovados por nome: {str(e)}")
        return []
    


# ======

def get_aprovados_by_curso(curso, table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = select(table).where(table.c.Curso == curso)

        with engine.connect() as conn:
            result = conn.execute(stmt)
            return result.fetchall()

    except SQLAlchemyError as e:
        print(f"Erro ao buscar aprovados por curso: {str(e)}")
        return []


def get_aprovados_by_semestre(semestre, table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = select(table).where(table.c.Semestre == semestre)

        with engine.connect() as conn:
            result = conn.execute(stmt)
            return result.fetchall()

    except SQLAlchemyError as e:
        print(f"Erro ao buscar aprovados por semestre: {str(e)}")
        return []


def get_aprovados_by_curso_categoria(curso, categoria, table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = select(table).where(
            (table.c.Curso == curso) &
            (table.c.Categoria == categoria)
        )

        with engine.connect() as conn:
            result = conn.execute(stmt)
            return result.fetchall()

    except SQLAlchemyError as e:
        print(f"Erro ao buscar por curso e categoria: {str(e)}")
        return []
    

    # =====================================================================



def get_aprovados_dataframe(table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = select(table)

        with engine.connect() as conn:
            result = conn.execute(stmt)
            rows = result.fetchall()

            # Converter para DataFrame
            df = pd.DataFrame(rows, columns=result.keys())


            # # =========================
            # # LIMPEZA DOS DADOS
            # # =========================
            # df.columns = df.columns.str.strip()

            # df["Curso"] = df["Curso"].astype(str).str.strip()
            # df["Semestre"] = df["Semestre"].astype(str).str.strip()
            # df["Categoria"] = df["Categoria"].astype(str).str.strip()

            # # Converter Nota
            # df["Nota"] = (
            #     df["Nota"]
            #     .astype(str)
            #     .str.replace(",", ".", regex=False)
            #     .str.extract(r"(\d+\.?\d*)")[0]
            # )
            # df["Nota"] = pd.to_numeric(df["Nota"], errors="coerce")

            # # Converter Posição
            # df["Posicao"] = (
            #     df["Posicao"]
            #     .astype(str)
            #     .str.extract(r"(\d+)")[0]
            # )
            # df["Posicao"] = pd.to_numeric(df["Posicao"], errors="coerce")

            # # df = df.replace({np.nan: None}) # o JSON padrão não aceita NaN, inf, etc. por isso troca por None. NO ENTANTO PRECISA INSTALAR NUMPY
            # # df = df.where(pd.notnull(df), None) # faz o mesmo que acima mas usa somente PANDAS
            # # faz uma substituição de valores nulos (NaN) dentro de um DataFrame do pandas
            # # O que acontece no código
            # # Onde o valor NÃO é nulo → ele permanece igual
            # # Onde o valor é nulo → ele vira None
            # data = df.where(df.notnull(), None).to_dict(orient="records") # tratamento de nulos + conversão do DataFrame para estrutura Python (lista de dicionários) usando o pandas.

            # return data

            return df

    except SQLAlchemyError as e:
        print(f"Erro ao gerar dataframe: {str(e)}")
        return None
    

def get_cursos_unicos(table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = select(table.c.Curso)

        with engine.connect() as conn:
            result = conn.execute(stmt)
            rows = result.fetchall()

            # Criar DataFrame
            df = pd.DataFrame(rows, columns=result.keys())

            # Aplicar lógica desejada
            cursos = sorted(df["Curso"].dropna().unique())

            return cursos

    except SQLAlchemyError as e:
        print(f"Erro ao buscar cursos únicos: {str(e)}")
        return []
    

def get_semestres_unicos(table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = select(table.c.Semestre)

        with engine.connect() as conn:
            result = conn.execute(stmt)
            rows = result.fetchall()

            # Criar DataFrame
            df = pd.DataFrame(rows, columns=result.keys())

            # Aplicar lógica desejada
            semestres = sorted(df["Semestre"].dropna().unique())

            return semestres

    except SQLAlchemyError as e:
        print(f"Erro ao buscar semestres únicos: {str(e)}")
        return []
    

def get_categorias_unicos(table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = select(table.c.Categoria)

        with engine.connect() as conn:
            result = conn.execute(stmt)
            rows = result.fetchall()

            # Criar DataFrame
            df = pd.DataFrame(rows, columns=result.keys())

            # Aplicar lógica desejada
            categorias = sorted(df["Categoria"].dropna().unique())

            return categorias

    except SQLAlchemyError as e:
        print(f"Erro ao buscar categorias únicos: {str(e)}")
        return []   

def get_quantidade_por_categoria_geral(table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = (
            select(
                table.c.Categoria,
                func.count().label("Quantidade")
            )
            .group_by(table.c.Categoria)
            # .order_by(table.c.Categoria)
            .order_by(func.count())  # 👈 ordem crescente pela quantidade
        )

        with engine.connect() as conn:
            result = conn.execute(stmt)
            return result.fetchall()

    except SQLAlchemyError as e:
        print(f"Erro ao contar registros por categoria (geral): {str(e)}")
        return []
    


def get_estatisticas_gerais(table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = select(
            func.count().label("TotalAprovados"),
            func.min(
                cast(
                    func.replace(table.c.Nota, ',', '.'),
                    Float
                )
            ).label("MenorNota"),
            func.avg(
                cast(
                    func.replace(table.c.Nota, ',', '.'),
                    Float
                )
            ).label("Media"),
            func.max(
                cast(
                    func.replace(table.c.Nota, ',', '.'),
                    Float
                )
            ).label("MaiorNota")
        )

        with engine.connect() as conn:
            result = conn.execute(stmt).first()

            return result

    except SQLAlchemyError as e:
        print(f"Erro ao calcular estatísticas gerais: {str(e)}")
        return None

# def get_estatisticas_gerais(table_name="aprovados"):
#     try:
#         table = Table(table_name, metadata, autoload_with=engine)

#         with engine.connect() as conn:
#             # =========================
#             # 🔹 Estatísticas principais
#             # =========================
#             stmt = select(
#                 func.count().label("TotalAprovados"),
#                 func.min(
#                     cast(
#                         func.replace(table.c.Nota, ',', '.'),
#                         Float
#                     )
#                 ).label("MenorNota"),
#                 func.avg(
#                     cast(
#                         func.replace(table.c.Nota, ',', '.'),
#                         Float
#                     )
#                 ).label("Media"),
#                 func.max(
#                     cast(
#                         func.replace(table.c.Nota, ',', '.'),
#                         Float
#                     )
#                 ).label("MaiorNota")
#             )

#             result = conn.execute(stmt).first()

#             # =========================
#             # 🔹 NOVO: Semestres
#             # =========================
#             stmt_semestres = select(table.c.Semestre).distinct()
#             semestres = conn.execute(stmt_semestres).scalars().all()

#             # Converter para float (ex: "2019.1" → 2019.1)
#             semestres_float = []
#             for s in semestres:
#                 try:
#                     semestres_float.append(float(str(s).strip()))
#                 except:
#                     continue  # ignora valores inválidos

#             if semestres_float:
#                 semestre_inicio = min(semestres_float)
#                 semestre_fim = max(semestres_float)
#             else:
#                 semestre_inicio = None
#                 semestre_fim = None

#             return {
#                 "TotalAprovados": result.TotalAprovados,
#                 "MenorNota": result.MenorNota,
#                 "Media": result.Media,
#                 "MaiorNota": result.MaiorNota,
#                 "SemestreInicio": semestre_inicio,
#                 "SemestreFim": semestre_fim
#             }

#     except SQLAlchemyError as e:
#         print(f"Erro ao calcular estatísticas gerais: {str(e)}")
#         return None
    



# def get_menor_nota_por_curso(table_name="aprovados"):
#     try:
#         table = Table(table_name, metadata, autoload_with=engine)

#         stmt = (
#             select(
#                 table.c.Curso,
#                 func.min(
#                     cast(
#                         func.replace(table.c.Nota, ',', '.'),
#                         Float
#                     )
#                 ).label("MenorNota")
#             )
#             .group_by(table.c.Curso)
#             .order_by(table.c.Curso)
#         )

#         with engine.connect() as conn:
#             result = conn.execute(stmt)
#             return result.fetchall()

#     except SQLAlchemyError as e:
#         print(f"Erro ao buscar menor nota por curso: {str(e)}")
#         return []
    

def get_menor_nota_por_curso(table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = (
            select(
                table.c.Curso,
                func.min(
                    cast(
                        func.replace(table.c.Nota, ',', '.'),
                        Float
                    )
                ).label("MenorNota")
            )
            .group_by(table.c.Curso)
            .order_by("MenorNota")  # 👈 ordena da menor para a maior nota
        )

        with engine.connect() as conn:
            result = conn.execute(stmt)
            return result.fetchall()

    except SQLAlchemyError as e:
        print(f"Erro ao buscar menor nota por curso: {str(e)}")
        return []
    

# def get_media_nota_por_curso(table_name="aprovados"):
#     try:
#         table = Table(table_name, metadata, autoload_with=engine)

#         stmt = (
#             select(
#                 table.c.Curso,
#                 func.avg(
#                     cast(
#                         func.replace(table.c.Nota, ',', '.'),
#                         Float
#                     )
#                 ).label("MediaNota")
#             )
#             .group_by(table.c.Curso)
#             .order_by(table.c.Curso)
#         )

#         with engine.connect() as conn:
#             result = conn.execute(stmt)
#             return result.fetchall()

#     except SQLAlchemyError as e:
#         print(f"Erro ao calcular média por curso: {str(e)}")
#         return []

def get_media_nota_por_curso(table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = (
            select(
                table.c.Curso,
                func.avg(
                    cast(
                        func.replace(table.c.Nota, ',', '.'),
                        Float
                    )
                ).label("MediaNota")
            )
            .group_by(table.c.Curso)
            .order_by("MediaNota")  # 👈 ordena da menor média para a maior
        )

        with engine.connect() as conn:
            result = conn.execute(stmt)
            return result.fetchall()

    except SQLAlchemyError as e:
        print(f"Erro ao calcular média por curso: {str(e)}")
        return []


# def get_maior_nota_por_curso(table_name="aprovados"):
#     try:
#         table = Table(table_name, metadata, autoload_with=engine)

#         stmt = (
#             select(
#                 table.c.Curso,
#                 func.max(
#                     cast(
#                         func.replace(table.c.Nota, ',', '.'),
#                         Float
#                     )
#                 ).label("MaiorNota")
#             )
#             .group_by(table.c.Curso)
#             .order_by(table.c.Curso)
#         )

#         with engine.connect() as conn:
#             result = conn.execute(stmt)
#             return result.fetchall()

#     except SQLAlchemyError as e:
#         print(f"Erro ao buscar maior nota por curso: {str(e)}")
#         return []
    

def get_maior_nota_por_curso(table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = (
            select(
                table.c.Curso,
                func.max(
                    cast(
                        func.replace(table.c.Nota, ',', '.'),
                        Float
                    )
                ).label("MaiorNota")
            )
            .group_by(table.c.Curso)
            .order_by("MaiorNota")  # 👈 ordena da menor para a maior MaiorNota
        )

        with engine.connect() as conn:
            result = conn.execute(stmt)
            return result.fetchall()

    except SQLAlchemyError as e:
        print(f"Erro ao buscar maior nota por curso: {str(e)}")
        return []    

# # # # # # # # # # # # # # # # # # # # # por CURSO # # # # # # # # # # # # # # # # # # # # # # # # # # # #     
def get_estatisticas_gerais_por_curso(curso, table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = select(
            func.count().label("TotalAprovados"),
            func.min(
                cast(
                    func.replace(table.c.Nota, ',', '.'),
                    Float
                )
            ).label("MenorNota"),
            func.avg(
                cast(
                    func.replace(table.c.Nota, ',', '.'),
                    Float
                )
            ).label("Media"),
            func.max(
                cast(
                    func.replace(table.c.Nota, ',', '.'),
                    Float
                )
            ).label("MaiorNota")
        ).where(
            table.c.Curso == curso
        )

        with engine.connect() as conn:
            result = conn.execute(stmt).first()

            return result

    except SQLAlchemyError as e:
        print(f"Erro ao calcular estatísticas gerais por curso: {str(e)}")
        return None



# # # # # # # # # # # # # # # # # # # # # FIM por CURSO # # # # # # # # # # # # # # # # # # # # # # # # # # # #     
# def get_quantidade_por_categoria_do_curso(curso, table_name="aprovados"):
#     try:
#         table = Table(table_name, metadata, autoload_with=engine)

#         stmt = (
#             select(
#                 table.c.Categoria,
#                 func.count().label("Quantidade")
#             )
#             .where(
#                 (table.c.Curso == curso)
#             )
#             .group_by(table.c.Categoria)
#             .order_by("Quantidade")  # 👈 ordena da menor para a maior Quantidade
#         )

#         with engine.connect() as conn:
#             result = conn.execute(stmt)
#             return result.fetchall()

#     except SQLAlchemyError as e:
#         print(f"Erro ao contar por categoria: {str(e)}")
#         return []


def get_quantidade_por_categoria_do_curso(curso, table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        with engine.connect() as conn:
            # 🔹 1. Buscar todas as categorias existentes
            todas_categorias = conn.execute(
                select(table.c.Categoria).distinct()
            ).scalars().all()

            # 🔹 2. Buscar quantidades filtradas (SEM semestre)
            stmt = (
                select(
                    table.c.Categoria,
                    func.count().label("Quantidade")
                )
                .where(table.c.Curso == curso)  # 👈 apenas curso
                .group_by(table.c.Categoria)
            )

            result = conn.execute(stmt).fetchall()

        # 🔹 3. Converter resultado em dicionário
        mapa = {row.Categoria: row.Quantidade for row in result}

        # 🔹 4. Completar categorias faltantes com 0
        lista_final = []
        for categoria in todas_categorias:
            quantidade = mapa.get(categoria, 0)
            lista_final.append({
                "Categoria": categoria,
                "Quantidade": quantidade
            })

        # 🔹 5. Ordenar pela quantidade (crescente)
        lista_final.sort(key=lambda x: x["Quantidade"])

        return lista_final

    except SQLAlchemyError as e:
        print(f"Erro ao contar por categoria: {str(e)}")
        return []
    
# # # # # # # # # # # # # # # # # # # # # CURSO e SENESTRE # # # # # # # # # # # # # # # # # # # # # # # # # # # #     

def get_estatisticas_gerais_por_curso_e_semestre(curso, semestre, table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = select(
            func.count().label("TotalAprovados"),
            func.min(
                cast(
                    func.replace(table.c.Nota, ',', '.'),
                    Float
                )
            ).label("MenorNota"),
            func.avg(
                cast(
                    func.replace(table.c.Nota, ',', '.'),
                    Float
                )
            ).label("Media"),
            func.max(
                cast(
                    func.replace(table.c.Nota, ',', '.'),
                    Float
                )
            ).label("MaiorNota")
        ).where(
            (table.c.Curso == curso) &
            (table.c.Semestre == semestre)
        )

        with engine.connect() as conn:
            result = conn.execute(stmt).first()

            return result

    except SQLAlchemyError as e:
        print(f"Erro ao calcular estatísticas por curso e semestre: {str(e)}")
        return None
    
# def get_quantidade_por_categoria_do_curso_no_semestre(curso, semestre, table_name="aprovados"):
#     try:
#         table = Table(table_name, metadata, autoload_with=engine)

#         stmt = (
#             select(
#                 table.c.Categoria,
#                 func.count().label("Quantidade")
#             )
#             .where(
#                 (table.c.Curso == curso) &
#                 (table.c.Semestre == semestre)
#             )
#             .group_by(table.c.Categoria)
#             .order_by("Quantidade")  # 👈 ordena da menor para a maior Quantidade
#         )

#         with engine.connect() as conn:
#             result = conn.execute(stmt)
#             return result.fetchall()

#     except SQLAlchemyError as e:
#         print(f"Erro ao contar por categoria: {str(e)}")
#         return []
    

def get_quantidade_por_categoria_do_curso_no_semestre(curso, semestre, table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        with engine.connect() as conn:
            # 🔹 1. Buscar todas as categorias existentes
            todas_categorias = conn.execute(
                select(table.c.Categoria).distinct()
            ).scalars().all()

            # 🔹 2. Buscar quantidades filtradas
            stmt = (
                select(
                    table.c.Categoria,
                    func.count().label("Quantidade")
                )
                .where(
                    (table.c.Curso == curso) &
                    (table.c.Semestre == semestre)
                )
                .group_by(table.c.Categoria)
            )

            result = conn.execute(stmt).fetchall()

        # 🔹 3. Converter resultado em dicionário
        mapa = {row.Categoria: row.Quantidade for row in result}

        # 🔹 4. Completar categorias faltantes com 0
        lista_final = []
        for categoria in todas_categorias:
            quantidade = mapa.get(categoria, 0)
            lista_final.append({
                "Categoria": categoria,
                "Quantidade": quantidade
            })

        # 🔹 5. Ordenar pela quantidade (crescente)
        lista_final.sort(key=lambda x: x["Quantidade"])

        return lista_final

    except SQLAlchemyError as e:
        print(f"Erro ao contar por categoria: {str(e)}")
        return []


# # # # # # # # # # # # # # # # # # # # # FIM CURSO e SENESTRE # # # # # # # # # # # # # # # # # # # # # # # # # # # #     


def get_menor_nota_por_categoria_todos_semestres(table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        # Query sem filtro de curso
        stmt = (
            select(
                table.c.Categoria,
                table.c.Semestre,
                func.min(
                    cast(
                        func.replace(table.c.Nota, ',', '.'),
                        Float
                    )
                ).label("MenorNota")
            )
            .group_by(table.c.Categoria, table.c.Semestre)
        )

        with engine.connect() as conn:
            result = conn.execute(stmt)
            rows = result.fetchall()
            df = pd.DataFrame(rows, columns=result.keys())

        if df.empty:
            return df

        # Limpeza básica
        df["Semestre"] = df["Semestre"].astype(str).str.strip()
        df["Categoria"] = df["Categoria"].astype(str).str.strip()

        # --- PREENCHIMENTO DE FALTANTES ---

        todos_semestres = df["Semestre"].unique()
        todas_categorias = df["Categoria"].unique()

        novo_index = pd.MultiIndex.from_product(
            [todas_categorias, todos_semestres],
            names=["Categoria", "Semestre"]
        )

        df = df.set_index(["Categoria", "Semestre"])
        df = df.reindex(novo_index, fill_value=0.0).reset_index()

        df = df.sort_values(by=["Categoria", "Semestre"])

        return df

    except SQLAlchemyError as e:
        print(f"Erro ao buscar menor nota por categoria (todos cursos): {str(e)}")
        return pd.DataFrame()



# def get_menor_nota_por_categoria_todos_semestres(curso, table_name="aprovados"):
#     try:
#         table = Table(table_name, metadata, autoload_with=engine)

#         stmt = (
#             select(
#                 table.c.Semestre,
#                 table.c.Categoria,
#                 func.min(
#                     cast(
#                         func.replace(table.c.Nota, ',', '.'),
#                         Float
#                     )
#                 ).label("MenorNota")
#             )
#             .where(
#                 table.c.Curso == curso
#             )
#             .group_by(
#                 table.c.Semestre,
#                 table.c.Categoria
#             )
#             .order_by(table.c.Semestre)
#         )

#         with engine.connect() as conn:
#             result = conn.execute(stmt)
#             rows = result.fetchall()

#             # Converter para DataFrame
#             df = pd.DataFrame(rows, columns=result.keys())
#             df["Semestre"] = df["Semestre"].str.strip()
#             df["Semestre"] = df["Semestre"].astype(str)
#             df = df.sort_values(by="Semestre")            
#             return df

#     except SQLAlchemyError as e:
#         print(f"Erro ao buscar menor nota por categoria (todos semestres): {str(e)}")
#         return []




# def get_menor_nota_por_categoria_todos_semestres(curso, table_name="aprovados"):
#     try:
#         table = Table(table_name, metadata, autoload_with=engine)

#         stmt = (
#             select(
#                 table.c.Categoria,
#                 table.c.Semestre,
#                 func.min(
#                     cast(
#                         func.replace(table.c.Nota, ',', '.'),
#                         Float
#                     )
#                 ).label("MenorNota")
#             )
#             .where(
#                 table.c.Curso == curso
#             )
#             .group_by(
#                 table.c.Categoria,
#                 table.c.Semestre
#             )
#             .order_by(
#                 table.c.Categoria,
#                 table.c.Semestre
#             )
#         )

#         with engine.connect() as conn:
#             result = conn.execute(stmt)
#             rows = result.fetchall()

#             # Converter para DataFrame
#             df = pd.DataFrame(rows, columns=result.keys())

#             if df.empty:
#                 return df

#             df["Semestre"] = df["Semestre"].astype(str).str.strip()
#             df["Categoria"] = df["Categoria"].astype(str).str.strip()

#             df = df.sort_values(by=["Categoria", "Semestre"])

#             return df

#     except SQLAlchemyError as e:
#         print(f"Erro ao buscar menor nota por categoria (todos semestres): {str(e)}")
#         return pd.DataFrame()    
    




import pandas as pd
from sqlalchemy import select, func, cast, Float, Table
from sqlalchemy.exc import SQLAlchemyError

def get_menor_nota_por_categoria_do_curso_para_todos_semestres(curso, table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        # 1. Query original para buscar os dados existentes
        stmt = (
            select(
                table.c.Categoria,
                table.c.Semestre,
                func.min(
                    cast(
                        func.replace(table.c.Nota, ',', '.'),
                        Float
                    )
                ).label("MenorNota")
            )
            .where(table.c.Curso == curso)
            .group_by(table.c.Categoria, table.c.Semestre)
        )

        with engine.connect() as conn:
            result = conn.execute(stmt)
            rows = result.fetchall()
            df = pd.DataFrame(rows, columns=result.keys())

        if df.empty:
            return df

        # Limpeza básica de strings
        df["Semestre"] = df["Semestre"].astype(str).str.strip()
        df["Categoria"] = df["Categoria"].astype(str).str.strip()

        # --- NOVA LÓGICA: PREENCHIMENTO DE VALORES FALTANTES ---

        # 2. Identifica todos os semestres e categorias únicos presentes no resultado
        todos_semestres = df["Semestre"].unique()
        todas_categorias = df["Categoria"].unique()

        # 3. Cria um MultiIndex com todas as combinações possíveis (Produto Cartesiano)
        novo_index = pd.MultiIndex.from_product(
            [todas_categorias, todos_semestres], 
            names=["Categoria", "Semestre"]
        )

        # 4. Reindexa o DataFrame
        # Definimos Categoria e Semestre como index para poder usar o reindex
        df = df.set_index(["Categoria", "Semestre"])
        
        # O reindex preenche as combinações que não existiam com NaN, depois trocamos por 0.0
        df = df.reindex(novo_index, fill_value=0.0).reset_index()

        # 5. Ordenação final para garantir a consistência
        df = df.sort_values(by=["Categoria", "Semestre"])

        return df

    except SQLAlchemyError as e:
        print(f"Erro ao buscar menor nota por categoria (todos semestres): {str(e)}")
        return pd.DataFrame()
    

# def get_menor_nota_por_categoria(curso, semestre, table_name="aprovados"):
#     try:
#         table = Table(table_name, metadata, autoload_with=engine)

#         stmt = (
#             select(
#                 table.c.Categoria,
#                 # func.min(table.c.Nota).label("MenorNota")
#                 func.min(cast(table.c.Nota, Float)).label("MenorNota")
#             )
#             .where(
#                 (table.c.Curso == curso) &
#                 (table.c.Semestre == semestre)
#             )
#             .group_by(table.c.Categoria)
#         )

#         with engine.connect() as conn:
#             result = conn.execute(stmt)
#             return result.fetchall()

#     except SQLAlchemyError as e:
#         print(f"Erro ao buscar menor nota por categoria: {str(e)}")
#         return []


def get_menor_nota_por_categoria(curso, semestre, table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        # 🔹 1. Todas as categorias únicas
        stmt_categorias = select(table.c.Categoria).distinct()

        # 🔹 2. Menor nota por categoria (com filtro)
        stmt_menor_nota = (
            select(
                table.c.Categoria,
                func.min(cast(table.c.Nota, Float)).label("MenorNota")
            )
            .where(
                (table.c.Curso == curso) &
                (table.c.Semestre == semestre)
            )
            .group_by(table.c.Categoria)
        )

        with engine.connect() as conn:
            categorias_result = conn.execute(stmt_categorias).fetchall()
            notas_result = conn.execute(stmt_menor_nota).fetchall()

            todas_categorias = [row.Categoria for row in categorias_result]

            notas_dict = {
                row.Categoria: row.MenorNota
                for row in notas_result
            }

            # 🔹 3. Montar resultado garantindo todas as categorias
            resultado_final = []
            for categoria in todas_categorias:
                menor_nota = notas_dict.get(categoria, 0.0)
                resultado_final.append({
                    "Categoria": categoria,
                    "MenorNota": menor_nota
                })

            # 🔹 4. Ordenar por categoria
            resultado_final.sort(key=lambda x: x["Categoria"])

            return resultado_final

    except SQLAlchemyError as e:
        print(f"Erro ao buscar menor nota por categoria: {str(e)}")
        return []


def get_menorMediaMaior_nota_por_categoria(curso, semestre, table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine, schema="dbo") # 🔥 ESSENCIAL no SQL Server
        # VER COMO AS COLUNAS ESTÃO SENDO VISTAS (CASE SENSITIVE)
        print("teste\n\n\n")
        print(table.c.keys())
        print("teste\n\n\n")

        # 🔹 Todas as categorias existentes
        stmt_categorias = select(table.c.Categoria).distinct()

        # 🔹 Agregações: menor, média e maior
        # stmt_notas = (
        #     select(
        #         table.c.Categoria,
        #         func.min(cast(table.c.Nota, Float)).label("MenorNota"),
        #         func.avg(cast(table.c.Nota, Float)).label("MediaNota"),
        #         func.max(cast(table.c.Nota, Float)).label("MaiorNota"),
        #     )
        #     .where(
        #         (table.c.Curso == curso) &
        #         (table.c.Semestre == semestre)
        #     )
        #     .group_by(table.c.Categoria)
        # )

        stmt_notas = (
            select(
                table.c.Categoria,
                func.min(text("TRY_CAST(Nota AS FLOAT)")).label("MenorNota"),
                func.avg(text("TRY_CAST(Nota AS FLOAT)")).label("MediaNota"),
                func.max(text("TRY_CAST(Nota AS FLOAT)")).label("MaiorNota"),
            )
            .where(
                (table.c.Curso == curso) &
                (table.c.Semestre == semestre)
            )
            .group_by(table.c.Categoria)
        )

        with engine.connect() as conn:
            categorias_result = conn.execute(stmt_categorias).fetchall()
            notas_result = conn.execute(stmt_notas).fetchall()

            todas_categorias = [r.Categoria for r in categorias_result]

            notas_dict = {
                r.Categoria: {
                    "MenorNota": r.MenorNota,
                    "MediaNota": r.MediaNota,
                    "MaiorNota": r.MaiorNota
                }
                for r in notas_result
            }

            resultado_final = []
            for categoria in todas_categorias:
                valores = notas_dict.get(categoria, {
                    "MenorNota": 0,
                    "MediaNota": 0,
                    "MaiorNota": 0
                })

                resultado_final.append({
                    "Categoria": categoria,
                    "MenorNota": float(valores["MenorNota"] or 0),
                    "MediaNota": float(valores["MediaNota"] or 0),
                    "MaiorNota": float(valores["MaiorNota"] or 0)
                })

            # 🔹 Ordenação por categoria
            resultado_final.sort(key=lambda x: x["Categoria"])

            return resultado_final

    except SQLAlchemyError as e:
        print(f"Erro ao buscar notas por categoria: {str(e)}")
        return []
    
# def get_menor_nota_por_categoria_dois_cursos(curso1, curso2, table_name="aprovados"):
#     try:
#         table = Table(table_name, metadata, autoload_with=engine)

#         stmt = (
#             select(
#                 table.c.Curso,
#                 table.c.Categoria,
#                 func.min(
#                     cast(
#                         func.replace(table.c.Nota, ',', '.'),
#                         Float
#                     )
#                 ).label("MenorNota")
#             )
#             .where(
#                 table.c.Curso.in_([curso1, curso2])
#             )
#             .group_by(
#                 table.c.Curso,
#                 table.c.Categoria
#             )
#             .order_by(
#                 table.c.Curso,
#                 table.c.Categoria
#             )
#         )

#         with engine.connect() as conn:
#             result = conn.execute(stmt)
#             return result.fetchall()

#     except SQLAlchemyError as e:
#         print(f"Erro ao buscar menor nota por categoria (dois cursos): {str(e)}")
#         return []
    
    
def get_menor_nota_por_categoria_dois_cursos(curso1, curso2, semestre, table_name="aprovados"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = (
            select(
                table.c.Curso,
                table.c.Categoria,
                func.min(
                    cast(
                        func.replace(table.c.Nota, ',', '.'),
                        Float
                    )
                ).label("MenorNota")
            )
            .where(
                (table.c.Curso.in_([curso1, curso2])) &
                (table.c.Semestre == semestre)
            )
            .group_by(
                table.c.Curso,
                table.c.Categoria
            )
            .order_by(
                table.c.Curso,
                table.c.Categoria
            )
        )

        with engine.connect() as conn:
            result = conn.execute(stmt)
            return result.fetchall()

    except SQLAlchemyError as e:
        print(f"Erro ao buscar menor nota por categoria (dois cursos com semestre): {str(e)}")
        return []
    

# # # # # # # # # # # # # # # # # # # # # ROTAS PARA O BLOG DA ATIVIDADE EM CLASSE (EXCLUIR DEPOIS) # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# =========================
# BLOG
# =========================

def insert_blog(dado, table_name="blog"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        with engine.begin() as conn:
            conn.execute(table.insert(), dado)

        return True

    except SQLAlchemyError as e:
        print(f"Erro ao inserir blog: {str(e)}")
        return False


def get_blogs(table_name="blog"):
    try:
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = select(table)

        with engine.connect() as conn:
            result = conn.execute(stmt)
            return result.fetchall()

    except SQLAlchemyError as e:
        print(f"Erro ao buscar blogs: {str(e)}")
        return []
    
# # # # # # # # # # # # # # # # # # # # # FIM DAS ROTAS PARA O BLOG DA ATIVIDADE EM CLASSE (EXCLUIR DEPOIS) # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
