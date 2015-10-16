# Copyright (C) 2015 Clemente Junior
#
# This file is part of SigeLib
#
# SigeLib is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

from sigelib import Environment

EXTRA_HOUR_ALERT = '[Hora Extra] {} ja esta trabalhando a {}! - Jornada de {}'
INTERJOURNEY_ALERT = ('[Interjornada Divergente] Empregado: {} tirou {}H de '
                      'interjornada!')
REST_ALERT = '[Intervalo Divergente] {} tirou intervalo de: {} H'
FIRST_JOURNEY_EXTRAPOLATED_ALERT = (
    '[Extrapolação da primeira Jornada] {} ja esta '
    'trabalhando a {}! - Jornada de {}')

SECOND_JOURNEY_EXTRAPOLATED_ALERT = (
    '[Extrapolação da segunda Jornada] {} ja esta '
    'trabalhando a {}! - Jornada de {}')
WITHOUT_CHECK_ENTRY_ALERT = ('[Sem Batida no Ponto de Entrada] {} Passou na '
                             'catraca às {} mas não tem registro no ponto.')

WITHOUT_CHECK_ON_40M_ALERT = ('[Sem Batida no Ponto] {} Passou na 1ª'
                              'catraca às {} mas não tem registro no ponto.')

WITHOUT_CHECK_EXIT_ALERT = ('[Sem Batida no Ponto de Saída] {} Passou na '
                            'catraca às {} mas não tem registro no ponto.')

QUERY_CHECKS = """
SELECT E.nome,
       A.dataregistro,
       D.descricao,
       f.codfunc,
       Replace (Replace (E.pis, '.', ''), '-', '') PIS
FROM   afd_0001 A,
       empregado E
       INNER JOIN toppontorep.dbo.funcionarios F
               ON ( Replace (Replace (F.pis, '.', ''), '-', '') = Replace (
               Replace (E.pis, '.', ''), '-', '') )
       INNER JOIN toppontorep.dbo.departamentos D
               ON ( F.coddepto = D.coddepto )
WHERE  CONVERT (INT, A.dataregistro) BETWEEN {0} AND {1}
       AND A.tiporegistro = 3
       AND Substring (A.dadosregistro, 24, 11) = Replace (Replace (E.pis,
       '.', ''), '-', '')
GROUP  BY f.codfunc,
          E.nome,
          A.dataregistro,
          D.descricao,
          E.pis
union all
SELECT E.nome,
       A.dataregistro,
       D.descricao,
       f.codfunc,
       Replace (Replace (E.pis, '.', ''), '-', '') PIS
FROM   afd_0002 A,
       empregado E
       INNER JOIN toppontorep.dbo.funcionarios F
               ON ( Replace (Replace (F.pis, '.', ''), '-', '') = Replace (
               Replace (E.pis, '.', ''), '-', '') )
       INNER JOIN toppontorep.dbo.departamentos D
               ON ( F.coddepto = D.coddepto )
WHERE  CONVERT (INT, A.dataregistro) BETWEEN {0} AND {1}
       AND A.tiporegistro = 3
       AND Substring (A.dadosregistro, 24, 11) = Replace (Replace (E.pis,
       '.', ''), '-', '')
GROUP  BY f.codfunc,
          E.nome,
          A.dataregistro,
          D.descricao,
          E.pis

ORDER  BY 1, 2
"""

QUERY_JOURNEY = """
 SELECT codhorario,
       CASE
         WHEN qt = 10 THEN CONVERT(TIME, ( seq2 - seq1 + seq4 - seq3 ))
         ELSE CONVERT(TIME, ( seq4 - seq1 ))
       END horas_jornada
FROM   (SELECT codhorario,
               Max(CASE
                     WHEN m.sequencia = 1 THEN m.marcacao
                   END)         seq1,
               Max(CASE
                     WHEN m.sequencia = 2 THEN m.marcacao
                   END)         seq2,
               Max(CASE
                     WHEN m.sequencia = 3 THEN m.marcacao
                   END)         seq3,
               Max(CASE
                     WHEN m.sequencia = 4 THEN m.marcacao
                   END)         seq4,
               Sum(m.sequencia) qt
        FROM   toppontorep.dbo.marcacoes m
        GROUP  BY codhorario) dados
"""
QUERY_HOURS_TABLE = """
 SELECT f.codfunc,
       HJ.sequencia,
       HJ.codhorario,
       CONVERT(DATE, JF.DTINICIO) DATA,
       JF.SequenciaInic
FROM   toppontorep.dbo.funcionarios F
       INNER JOIN toppontorep.dbo.jornadas_func JF
               ON ( F.codfunc = JF.codfunc )
       INNER JOIN toppontorep.dbo.horarios_jornada HJ
               ON ( HJ.codjornada = JF.codjornada )
WHERE  JF.dtinicio = (SELECT Max (dtinicio)
                      FROM   toppontorep.dbo.jornadas_func
                      WHERE  codfunc = JF.codfunc
                             AND dtinicio <= Getdate())
       AND codhorario IS NOT NULL
ORDER  BY codfunc, sequencia
"""

QUERY_OCCURRENCE_HOURS_TABLE = """
      SELECT F.CODFUNC,
      CONVERT(DATE, JF.DTINICIO) DATA,
      HJ.sequencia,
      HJ.codhorario,
      JF.SequenciaInic
    FROM   toppontorep.dbo.funcionarios F
           INNER JOIN toppontorep.dbo.jornadas_func JF
                   ON ( F.codfunc = JF.codfunc )
           INNER JOIN toppontorep.dbo.horarios_jornada HJ
                   ON ( HJ.codjornada = JF.codjornada )
    WHERE  codhorario IS NOT NULL
    ORDER  BY codfunc, JF.dtinicio asc, sequencia
    """

QUERY_GATE = """
SELECT Replace (Replace (F.pis, '.', ''), '-', ''), A.DATA_ACESSO, A.SENTIDO
FROM   dbo.acessos A, mr_acesso_cn.dbo.funcionarios F
where f.codigo_funcionario = a.codigo_funcionario
AND A.CODIGO_INNER = 1 AND A.DATA_ACESSO between '{}' AND '{}'
 order by 1 ASC,2 DESC
"""

QUERY_GATE2 = """
SELECT Replace (Replace (F.pis, '.', ''), '-', ''), A.DATA_ACESSO, A.SENTIDO
FROM   dbo.acessos A, mr_acesso_cn.dbo.funcionarios F
where f.codigo_funcionario = a.codigo_funcionario
AND A.CODIGO_INNER = 2 AND A.DATA_ACESSO between '{}' AND '{}'
 order by 1 ASC,2 DESC
"""

QUERY_PIS = """
SELECT replace(replace(F.PIS, '.', ''), '-', ''),
       F.NOME + ' [' + D.descricao + ']'
FROM   toppontorep.dbo.funcionarios F, toppontorep.dbo.departamentos D
               where F.coddepto = D.coddepto
"""

CONSULTA_MANIFESTOS = """
  SELECT   CODFILIAL, NUMTRANSACAO, DATAHORAGERACAO, SITUACAOMDFE
    FROM   (SELECT   C.CODFILIAL, C.NUMTRANSACAO, C.DATAHORAGERACAO,
    C.SITUACAOMDFE
              FROM   PCMANIFESTOELETRONICOC C, PCMANIFESTOELETRONICOI I,
              PCNFSAID N, PCFILIAL F, PCFORNEC FE
             WHERE   C.NUMTRANSACAO = I.NUMTRANSACAO AND I.NUMTRANSVENDA =
             N.NUMTRANSVENDA AND C.CODFILIAL = F.CODIGO AND F.CODFORNEC =
             FE.CODFORNEC
            UNION
            SELECT   C.CODFILIAL, C.NUMTRANSACAO, C.DATAHORAGERACAO,
            C.SITUACAOMDFE
              FROM   PCMANIFESTOELETRONICOC C, PCMANIFESTOELETRONICOI I,
              PCFILIAL F, PCFORNEC FE
             WHERE       C.NUMTRANSACAO = I.NUMTRANSACAO
                     AND C.CODFILIAL = F.CODIGO
                     AND F.CODFORNEC = FE.CODFORNEC
                     AND NOT EXISTS (SELECT   NUMTRANSVENDA
                                       FROM   PCNFSAID
                                      WHERE   PCNFSAID.NUMTRANSVENDA =
                                      I.NUMTRANSVENDA))
   WHERE   CODFILIAL = '1' AND SITUACAOMDFE IN (100) AND DATAHORAGERACAO
   BETWEEN TRUNC (SYSDATE, 'YYYY') AND TRUNC (SYSDATE) - 7
ORDER BY   DATAHORAGERACAO
"""

QUERY_VERIFY_DRIVERS = """
  SELECT F.Nome,
         B.DataHora
    FROM Bilhetes B, Funcionarios F
   where b.codfunc = f.codfunc
     and b.DataHora between '{}' and '{}'
order by 1, 2
"""

QUERY_VERIFY_DRIVERS_WO_CHECKS = """
              SELECT codfunc, NOME
from Funcionarios where DtDemissao is null and CodFunc not in (
SELECT B.CodFunc FROM Bilhetes B, Funcionarios F
where b.codfunc = f.codfunc
and b.DataHora between DATEADD(day, -4, getdate()) and getdate())
and codfunc not in (select codfunc from afastamentos where
   (dtinicio <= DATEADD(day, -4, getdate()) and dtfim >= getdate())
or (dtinicio <= DATEADD(day, -4, getdate()) and
dtfim >= DATEADD(day, -4, getdate()))
or (dtinicio <= getdate() and dtfim >= getdate())
or (dtinicio >= DATEADD(day, -4, getdate()) and dtfim <= getdate()))
and codfunc not in (select codfunc from abonos where
data between DATEADD(day, -4, getdate()) and getdate())"""

QUERY_VERIFY_FAULTS = """
    SELECT convert(date, a.data) as data, f.nome, ma.descricao, c.descricao,
    d.descricao
  FROM abonos a, funcionarios f, motivosabono ma, cargos c, departamentos d
  where a.codmotivo = ma.codmotivo and a.codfunc = f.codfunc and a.codmotivo
  IN (1, 5, 6)
  and c.codcargo = f.codcargo
  and d.coddepto = f.coddepto
  and data between getdate() - 90 and getdate()
  order by 1, 3, 2"""

QUERY_OS_PRODUCTIVITY = """
     SELECT   E.NOME || ';' || E.FUNCAO,
     COUNT(DISTINCT TO_CHAR(PCMOVENDPEND.NUMOS,'FM0000000000') || TO_CHAR(
     PCMOVENDPEND.CODENDERECO,'FM0000000000')) QTR,
           TRUNC (PCMOVENDPEND.DTINICIOOS) DATA, 'SEPARACAO'
    FROM   PCPRODUT, PCMOVENDPEND, PCEMPR, PCPERFILUSUARIOWMS, PCEMPR E
   WHERE       PCPRODUT.CODPROD = PCMOVENDPEND.CODPROD
           AND PCMOVENDPEND.CODFUNCOS = PCEMPR.MATRICULA
           AND E.MATRICULA = PCMOVENDPEND.CODFUNCOS
           AND PCEMPR.CODIGOPERFIL = PCPERFILUSUARIOWMS.CODIGOPERFIL
           AND PCMOVENDPEND.CODFILIAL = '1'
           AND PCMOVENDPEND.DTINICIOOS IS NOT NULL
           AND PCMOVENDPEND.DTFIMSEPARACAO IS NOT NULL
           AND PCMOVENDPEND.DTESTORNO IS NULL
           AND PCMOVENDPEND.CODOPER NOT IN ('SA', 'EA')
           AND TRUNC (PCMOVENDPEND.DTINICIOOS) BETWEEN TRUNC (SYSDATE) - 30
           AND TRUNC (SYSDATE)
           AND PCMOVENDPEND.NUMOS IS NOT NULL
           AND PCMOVENDPEND.POSICAO = 'C'
           AND PCMOVENDPEND.CODFUNCOS IS NOT NULL
GROUP BY   PCMOVENDPEND.CODFUNCOS, PCEMPR.CODIGOPERFIL,
PCPERFILUSUARIOWMS.DESCRICAOPERFIL,
           TRUNC (PCMOVENDPEND.DTINICIOOS), E.NOME, E.FUNCAO
UNION ALL
  SELECT   E.NOME || ';' ||
  E.FUNCAO, COUNT(DISTINCT TO_CHAR(PCMOVENDPEND.NUMOS,'FM0000000000') ||
  TO_CHAR(PCMOVENDPEND.CODENDERECO,'FM0000000000')) QTR,
           TRUNC (PCMOVENDPEND.DTINICIOOS) DATA, 'EMBALADOR'
    FROM   PCPRODUT, PCMOVENDPEND, PCEMPR, PCPERFILUSUARIOWMS, PCEMPR E
   WHERE       PCPRODUT.CODPROD = PCMOVENDPEND.CODPROD
           AND PCMOVENDPEND.CODFUNCEMBALADOR = PCEMPR.MATRICULA
           AND PCEMPR.CODIGOPERFIL = PCPERFILUSUARIOWMS.CODIGOPERFIL
           AND PCMOVENDPEND.CODFILIAL = '1'
           AND E.MATRICULA = PCMOVENDPEND.CODFUNCEMBALADOR
           AND PCMOVENDPEND.DTINICIOOS IS NOT NULL
           AND PCMOVENDPEND.DTFIMSEPARACAO IS NOT NULL
           AND PCMOVENDPEND.DTESTORNO IS NULL
           AND PCMOVENDPEND.CODOPER NOT IN ('SA', 'EA')
           AND TRUNC (PCMOVENDPEND.DTINICIOOS) BETWEEN TRUNC (SYSDATE) - 30
           AND TRUNC (SYSDATE)
           AND PCMOVENDPEND.NUMOS IS NOT NULL
           AND PCMOVENDPEND.POSICAO = 'C'
           AND PCMOVENDPEND.CODFUNCEMBALADOR IS NOT NULL
GROUP BY   PCMOVENDPEND.CODFUNCEMBALADOR, PCEMPR.CODIGOPERFIL,
PCPERFILUSUARIOWMS.DESCRICAOPERFIL,
           TRUNC (PCMOVENDPEND.DTINICIOOS), E.NOME, E.FUNCAO
UNION ALL
  SELECT   E.NOME || ';' || E.FUNCAO
               FUNCIONARIO,
               COUNT(DISTINCT TO_CHAR(PCMOVENDPEND.NUMOS,'FM0000000000') ||
               TO_CHAR(PCMOVENDPEND.CODENDERECO,'FM0000000000')) QTR, TRUNC (
               PCMOVENDPEND.DTINICIOCONFERENCIA) DATA, 'CONFERENCIA'
    FROM   PCPRODUT, PCMOVENDPEND, PCEMPR, PCPERFILUSUARIOWMS, PCEMPR E
   WHERE       PCPRODUT.CODPROD = PCMOVENDPEND.CODPROD
           AND PCMOVENDPEND.CODFUNCCOFERENTE = PCEMPR.MATRICULA
           AND PCEMPR.CODIGOPERFIL = PCPERFILUSUARIOWMS.CODIGOPERFIL
           AND PCMOVENDPEND.CODFILIAL = '1'
           AND E.MATRICULA = NVL (PCMOVENDPEND.CODFUNCCOFERENTE,
           PCMOVENDPEND.CODFUNCCONF)
           AND PCMOVENDPEND.DTINICIOOS IS NOT NULL
           AND PCMOVENDPEND.DTFIMSEPARACAO IS NOT NULL
           AND PCMOVENDPEND.DTESTORNO IS NULL
           AND PCMOVENDPEND.CODOPER NOT IN ('SA', 'EA')
           AND TRUNC (PCMOVENDPEND.DTINICIOCONFERENCIA) BETWEEN TRUNC (
           SYSDATE) - 30 AND TRUNC (SYSDATE)
           AND PCMOVENDPEND.NUMOS IS NOT NULL
           AND PCMOVENDPEND.POSICAO = 'C'
           AND (PCMOVENDPEND.CODFUNCCOFERENTE IS NOT NULL OR
           PCMOVENDPEND.CODFUNCCONF IS NOT NULL)
GROUP BY   PCMOVENDPEND.CODFUNCCOFERENTE, PCMOVENDPEND.CODFUNCCONF,
PCEMPR.CODIGOPERFIL,
           PCPERFILUSUARIOWMS.DESCRICAOPERFIL, TRUNC (
           PCMOVENDPEND.DTINICIOCONFERENCIA), E.NOME, E.FUNCAO"""

QUERY_WEEK_JOURNEY = """select nome,
max (case when sequencia = 1 then horas_jornada1 end) seg1,
max (case when sequencia = 1 then horas_jornada2 end) seg2,
max (case when sequencia = 2 then horas_jornada1 end) ter1,
max (case when sequencia = 2 then horas_jornada2 end) ter2,
max (case when sequencia = 3 then horas_jornada1 end) qua1,
max (case when sequencia = 3 then horas_jornada2 end) qua2,
max (case when sequencia = 4 then horas_jornada1 end) qui1,
max (case when sequencia = 4 then horas_jornada2 end) qui2,
max (case when sequencia = 5 then horas_jornada1 end) sex1,
max (case when sequencia = 5 then horas_jornada2 end) sex2,
max (case when sequencia = 6 then horas_jornada1 end) sab1,
max (case when sequencia = 6 then horas_jornada2 end) sab2
 from
(SELECT codhorario,
       CASE
         WHEN qt = 10 THEN CONVERT(TIME, ( seq2 - seq1))
         ELSE CONVERT(TIME, ( seq4 - seq1 ))
       END horas_jornada1,
       CASE
         WHEN qt = 10 THEN CONVERT(TIME, (seq4 - seq3 ))
       END horas_jornada2
FROM   (SELECT codhorario,
               Max(CASE
                     WHEN m.sequencia = 1 THEN m.marcacao
                   END)         seq1,
               Max(CASE
                     WHEN m.sequencia = 2 THEN m.marcacao
                   END)         seq2,
               Max(CASE
                     WHEN m.sequencia = 3 THEN m.marcacao
                   END)         seq3,
               Max(CASE
                     WHEN m.sequencia = 4 THEN m.marcacao
                   END)         seq4,
               Sum(m.sequencia) qt
        FROM   toppontorep.dbo.marcacoes m
        GROUP  BY codhorario) dados) th,
        (  SELECT F.CODFUNC, F.nome,
  CONVERT(DATE, JF.DTINICIO) DATA,
  HJ.sequencia,
  HJ.codhorario,
  JF.SequenciaInic
FROM   toppontorep.dbo.funcionarios F
       INNER JOIN toppontorep.dbo.jornadas_func JF
               ON ( F.codfunc = JF.codfunc )
       INNER JOIN toppontorep.dbo.horarios_jornada HJ
               ON ( HJ.codjornada = JF.codjornada )
               INNER JOIN toppontorep.dbo.jornadas JOR
               ON (JF.codjornada = JOR.codjornada and JOR.Descricao not in ('APRENDIZ 12 QUA A SEX 08:00-12:00',
'APRENDIZ 12 QUI A SEX 13:30-17:30 SAB 08:30-12:30',
'APRENDIZ 12 SEG A QUA 13:30-17:30',
'APRENDIZ 16 QUA A SAB 08:00-12:00',
'APRENDIZ 16 QUA A SEX 13:30-17:30 SAB 08:00-12:00',
'APRENDIZ 16 SEG A QUI 13:30-17:30',
'APRENDIZ 16 SEG A QUI 08:00-12:00'))
WHERE  codhorario IS NOT NULL
and JF.DTINICIO = (select max(DTINICIO) from toppontorep.dbo.jornadas_func
where codfunc = f.codfunc)
and f.dtdemissao is null
) tf
where th.codhorario = tf.codhorario
group by codfunc, nome
order by nome
"""

SCRIPTS_DAILY_UPDATE = ["""INSERT INTO
[POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[PERFIS] (DESCRICAO, PASSE_LIVRE)
select DISTINCT perfil, 0
    FROM (select        j.codjornada, j.descricao as perfil,
                max(case when (hj.sequencia = 1) then 1 else 0 end) segunda,
                max(case when (hj.sequencia = 2) then 1 else 0 end) terca,
                max(case when (hj.sequencia = 3) then 1 else 0 end) quarta,
                max(case when (hj.sequencia = 4) then 1 else 0 end) quinta,
                max(case when (hj.sequencia = 5) then 1 else 0 end) sexta,
                max(case when (hj.sequencia = 6) then 1 else 0 end) sabado,
                max(case when (hj.sequencia = 7) then 1 else 0 end) domingo,
                max(case when (M.sequencia = 1) then CONVERT(VARCHAR(5),
                M.marcacao, 108) end) ENTRADA1,
                max(case when (M.sequencia = 2) then CONVERT(VARCHAR(5),
                M.marcacao, 108) end) SAIDA1,
                max(case when (M.sequencia = 3) then CONVERT(VARCHAR(5),
                M.marcacao, 108) end) ENTRADA2,
                max(case when (M.sequencia = 4) then CONVERT(VARCHAR(5),
                M.marcacao, 108) end) SAIDA2
    from        jornadas j
                    inner join horarios_jornada hj
                        on (j.codjornada = hj.codjornada)
                    inner join marcacoes m
                        on (hj.codhorario = m.codhorario)
                    inner join horarios h
                        on (m.codhorario = h.codhorario)
    group by    j.codjornada, j.descricao, h.descricao ) data where perfil
    not in
    (select descricao from
    [POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[PERFIS])""", """INSERT INTO
[POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[HORARIOS]
(CODIGO_PERFIL, SEGUNDA, TERCA, QUARTA, QUINTA, SEXTA, SABADO, DOMINGO,
                        INICIO_TURNO_1, FIM_TURNO_1, INICIO_TURNO_2,
                        FIM_TURNO_2)
select (select codigo_perfil from
[POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[perfis]
where descricao = perfil) codigo_perfil,
segunda, terca, quarta, quinta, sexta, sabado, domingo, ENTRADA1,
case when saida1 is null and saida2 is not null then saida2 else SAIDA1 end
saida2,
ENTRADA2,
case when ENTRADA2 is null then null else SAIDA2 end saida2
 from (
    select        j.codjornada, j.descricao as perfil,
                max(case when (hj.sequencia = 1) then 1 else 0 end) segunda,
                max(case when (hj.sequencia = 2) then 1 else 0 end) terca,
                max(case when (hj.sequencia = 3) then 1 else 0 end) quarta,
                max(case when (hj.sequencia = 4) then 1 else 0 end) quinta,
                max(case when (hj.sequencia = 5) then 1 else 0 end) sexta,
                max(case when (hj.sequencia = 6) then 1 else 0 end) sabado,
                max(case when (hj.sequencia = 7) then 1 else 0 end) domingo,
                max(case when (M.sequencia = 1) then CONVERT(VARCHAR(5),
                M.marcacao, 108) end) ENTRADA1,
                max(case when (M.sequencia = 2) then CONVERT(VARCHAR(5),
                M.marcacao, 108) end) SAIDA1,
                max(case when (M.sequencia = 3) then CONVERT(VARCHAR(5),
                M.marcacao, 108) end) ENTRADA2,
                max(case when (M.sequencia = 4) then CONVERT(VARCHAR(5),
                M.marcacao, 108) end) SAIDA2
    from        jornadas j
                    inner join horarios_jornada hj
                        on (j.codjornada = hj.codjornada)
                    inner join marcacoes m
                        on (hj.codhorario = m.codhorario)
                    inner join horarios h
                        on (m.codhorario = h.codhorario)
    group by    j.codjornada, j.descricao, h.descricao
    ) data
    WHERE (select codigo_perfil from
    [POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[perfis]
    where descricao = perfil) NOT IN
(SELECT CODIGO_PERFIL FROM
[POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[HORARIOS])
ORDER BY codjornada""", """INSERT INTO
[POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[FUNCIONARIOS]
(CODIGO_FUNCIONARIO, CODIGO_PERFIL, CODIGO_BIOMETRICO, CODIGO_CARTAO, NOME,
PIS, CARTEIRA, MATRICULA, ADMISSAO, DEMISSAO, UTILIZA_BIOMETRIA,
                          LIVRE_CIRCULACAO)
select codfunc, (select codigo_perfil from
[POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[perfis] where
descricao = perfil) codigo_perfil,
matricula cod_bio, matricula cod_car, nome, pis, carteira, matricula,
CONVERT(SMALLDATETIME,dtadmissao),
CONVERT(SMALLDATETIME,DTDEMISSAO), 1 usa_bio, 0 livre
 from (select j.descricao as perfil, fj.codfunc, f.nome, f.pis,
     f.carteira, f.matricula, f.dtadmissao, f.dtdemissao
    from        jornadas j
                    inner join jornadas_func fj
                        on (j.codjornada = fj.codjornada)
                    inner join funcionarios f
                        on (fj.codfunc = f.codfunc)
        where
        Fj.dtinicio = (select MAX(dtinicio)
                         from jornadas_func
                        where codfunc = f.codfunc)
) data
where codfunc not in (SELECT CODIGO_FUNCIONARIO FROM
[POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[FUNCIONARIOS])""", """INSERT INTO
[POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[TEMPLATES]
(CODIGO_FUNCIONARIO ,CODIGO_BIOMETRICO ,TEMPLATE_1 ,TEMPLATE_2)
SELECT f.CODIGO_FUNCIONARIO,IdBiometrico,template1,template2 FROM
[GERENCIADORINNERREP].[dbo].[Templates] t inner join
[POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[FUNCIONARIOS] f
    on (t.idbiometrico = f.MATRICULA)
    where F.CODIGO_FUNCIONARIO NOT IN (SELECT CODIGO_FUNCIONARIO FROM
    [POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[TEMPLATES])
    and f.CODIGO_FUNCIONARIO is not null""", """DELETE FROM
[POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[TEMPLATES_ENVIOS]
WHERE TEMPLATE_1 IS NULL""", """INSERT INTO
[POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[TEMPLATES_ENVIOS]
              (CODIGO_FUNCIONARIO, CODIGO_INNER ,CODIGO_BIOMETRICO ,
              TEMPLATE_1 ,TEMPLATE_2, TEMPLATE_ENVIADO)
SELECT CODIGO_FUNCIONARIO, 1,CODIGO_BIOMETRICO,TEMPLATE_1,TEMPLATE_2,0
  FROM [POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[Templates]
  where CODIGO_FUNCIONARIO not in (select CODIGO_FUNCIONARIO from
  [POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[TEMPLATES_ENVIOS] where
  CODIGO_INNER = 1)""", """INSERT INTO
[POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[TEMPLATES_ENVIOS]
(CODIGO_FUNCIONARIO, CODIGO_INNER ,CODIGO_BIOMETRICO ,TEMPLATE_1 ,
TEMPLATE_2, TEMPLATE_ENVIADO)
SELECT CODIGO_FUNCIONARIO, 2,CODIGO_BIOMETRICO,TEMPLATE_1,TEMPLATE_2,0
  FROM [POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[Templates]
  where CODIGO_FUNCIONARIO not in (select CODIGO_FUNCIONARIO from
  [POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[TEMPLATES_ENVIOS] where
  CODIGO_INNER = 2)""",
                        """if exists (select * from INFORMATION_SCHEMA.TABLES where
                                      TABLE_NAME = '#temp_func')    drop table #temp_func;""",
                        """DECLARE @cod_func AS INT;
                        DECLARE @perfil_atual AS INT;
                        DECLARE @perfil_novo AS INT;
                        SET ROWCOUNT 0;
                        (SELECT *
                         INTO   #temp_func
                         FROM   (SELECT codfunc,
                                        (SELECT codigo_perfil
                                         FROM   [POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[perfis]
                                         WHERE  descricao = perfil) AS codigo_perfil,
                                        (SELECT codigo_perfil
                                         FROM
                                         [POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[FUNCIONARIOS]
                                         WHERE  CODFUNC = CODIGO_FUNCIONARIO) AS PERFIL_ATUAL,
                                        matricula AS cod_bio,
                                        nome
                                 FROM   (SELECT j.descricao AS perfil,
                                                fj.codfunc,
                                                f.nome,
                                                f.pis,
                                               f.carteira,
                                                f.matricula,
                                                f.dtadmissao,
                                                f.dtdemissao
                                         FROM   jornadas AS j
                                                INNER JOIN
                                                jornadas_func AS fj
                                                ON (j.codjornada = fj.codjornada)
                                                INNER JOIN
                                                funcionarios AS f
                                                ON (fj.codfunc = f.codfunc)
                                         WHERE  Fj.dtinicio = (SELECT MAX(dtinicio)
                                                               FROM   jornadas_func
                                                               WHERE  codfunc = f.codfunc AND
                                                               dtinicio <= GETDATE())) AS data) AS X
                         WHERE  CODIGO_PERFIL <> PERFIL_ATUAL);
                        SET ROWCOUNT 1;
                        SELECT @cod_func = codfunc,
                               @perfil_novo = codigo_perfil
                        FROM   #temp_func;
                        WHILE @@rowcount <> 0
                            BEGIN
                                SET ROWCOUNT 0;
                                UPDATE  [POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[FUNCIONARIOS]
                                    SET CODIGO_PERFIL = @perfil_novo
                                WHERE   CODIGO_FUNCIONARIO = @cod_func;
                                DELETE #temp_func
                                WHERE  codfunc = @cod_func;
                                SET ROWCOUNT 1;
                                SELECT @cod_func = codfunc,
                                       @perfil_atual = perfil_atual,
                                       @perfil_novo = codigo_perfil
                                FROM   #temp_func;
                            END
                        SET ROWCOUNT 0;""", """UPDATE [POSEIDON\SQLEXPRESS].[mr_acesso_cn].[dbo].[HORARIOS] SET
HORARIOS.INTERVALO_MINIMO = case when (DBO.HORA_MINUTOS(INICIO_TURNO_2) - DBO.HORA_MINUTOS(FIM_TURNO_1)) <= 65 then 65
else (DBO.HORA_MINUTOS(INICIO_TURNO_2) - DBO.HORA_MINUTOS(FIM_TURNO_1)) - 5 end
WHERE (HORARIOS.FIM_TURNO_1 IS NOT NULL) AND (HORARIOS.INICIO_TURNO_2 IS NOT NULL)"""]

MANIFEST_ROW = "[Manifesto Atrasado] Transação: {}, Gerado: {}\n"

ENV = Environment(True)
if ENV.production:
    FPP_XMPP_RECIPIENTS = ["clemente@casanorte.vpn", "gleyber@casanorte.vpn",
                           "eleni@casanorte.vpn", "irinaldo@casanorte.vpn"]
    GLEYBER_XMPP_RECIPIENT = ["gleyber@casanorte.vpn"]
    GLEYBER_MAIL_RECIPIENT = ['gleyber@casanorte.com.br',
                              'cpd@casanorte.com.br']
    MANAGERS_MAIL_RECIPIENT = ['gleyber@casanorte.com.br',
                               'cpd@casanorte.com.br',
                               'glauber@casanorte.com.br']
    MANAGERS_XMPP_RECIPIENT = ['gleyber@casanorte.vpn',
                               'clemente@casanorte.vpn',
                               'glauber@casanorte.vpn']
    NORMAL_XMPP_RECIPIENTS = ['clemente@casanorte.vpn',
                              'glauber@casanorte.vpn',
                              'pessoal2@casanorte.vpn', 'madjal@casanorte.vpn',
                              'marjory@casanorte.vpn', 'abraao@casanorte.vpn',
                              'mesariocentral@casanorte.vpn',
                              'pessoal@casanorte.vpn', 'daniel@casanorte.vpn',
                              'cibelec@casanorte.vpn', 'rh@casanorte.vpn',
                              'gerenteloja@casanorte.vpn',
                              'eleni@casanorte.vpn',
                              'marceloe@casanorte.vpn', 'pedrop@casanorte.vpn',
                              'wms@casanorte.vpn', 'gerenteloja@casanorte.vpn']
else:
    FPP_XMPP_RECIPIENTS = ["dev@casanorte.vpn"]
    GLEYBER_XMPP_RECIPIENT = ["clemente@casanorte.vpn"]
    GLEYBER_MAIL_RECIPIENT = ['sige@casanorte.com.br']

    MANAGERS_MAIL_RECIPIENT = ['sige@casanorte.com.br']
    MANAGERS_XMPP_RECIPIENT = ['dev@casanorte.vpn']
    NORMAL_XMPP_RECIPIENTS = ['dev@casanorte.vpn']

EHIS = 11 * 60 * 60
THIS = 12 * 60 * 60
