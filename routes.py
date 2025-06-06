from flask import render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date 
from sqlalchemy import and_ 

def configure_routes(app, db):
   
    from models import Bem, Usuario, Ambiente, Movimentacao

    @app.route('/')
    def index():
    
        return render_template('index.html')

    @app.route('/bens')
    def listar_bens():
        bens = Bem.query.all()
        return render_template('bens/listar.html', bens=bens)

    @app.route('/bens/criar', methods=['GET', 'POST'])
    def criar_bem():
        if request.method == 'POST':
            tag_rfid = request.form['tag_rfid']
            nome = request.form['nome']
            descricao = request.form['descricao']
            numero_serie = request.form['numero_serie']
            id_ambiente_atual = request.form['id_ambiente_atual']
            data_aquisicao = request.form['data_aquisicao']
            valor_aquisicao = request.form['valor_aquisicao']
            status = request.form['status']

            try:
                novo_bem = Bem(
                    tag_rfid=tag_rfid,
                    nome=nome,
                    descricao=descricao,
                    numero_serie=numero_serie,
                    id_ambiente_atual=id_ambiente_atual if id_ambiente_atual else None,
                    data_aquisicao=datetime.strptime(data_aquisicao, '%Y-%m-%d').date() if data_aquisicao else None,
                    valor_aquisicao=float(valor_aquisicao) if valor_aquisicao else None,
                    status=status
                )
                db.session.add(novo_bem)
                db.session.commit()
                flash('Bem criado com sucesso!', 'success')
                return redirect(url_for('listar_bens'))
            except IntegrityError:
                db.session.rollback()
                flash('Erro: A tag RFID ou número de série já existe.', 'danger')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar bem: {e}', 'danger')

        ambientes = Ambiente.query.all() 
        return render_template('bens/criar.html', ambientes=ambientes)

    @app.route('/bens/editar/<int:id_bem>', methods=['GET', 'POST'])
    def editar_bem(id_bem):
        bem = Bem.query.get_or_404(id_bem)
        if request.method == 'POST':
            bem.nome = request.form['nome']
            bem.descricao = request.form['descricao']
            bem.numero_serie = request.form['numero_serie']
            bem.id_ambiente_atual = request.form['id_ambiente_atual'] if request.form['id_ambiente_atual'] else None
            # Tenta converter a data de aquisição, se não for None ou string vazia
            bem.data_aquisicao = datetime.strptime(request.form['data_aquisicao'], '%Y-%m-%d').date() if request.form['data_aquisicao'] else None
            # Tenta converter o valor de aquisição, se não for None ou string vazia
            bem.valor_aquisicao = float(request.form['valor_aquisicao']) if request.form['valor_aquisicao'] else None
            bem.status = request.form['status']

            try:
                db.session.commit()
                flash('Bem atualizado com sucesso!', 'success')
                return redirect(url_for('listar_bens'))
            except IntegrityError:
                db.session.rollback()
                flash('Erro: Número de série já existe.', 'danger')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar bem: {e}', 'danger')
        
        ambientes = Ambiente.query.all()
        return render_template('bens/editar.html', bem=bem, ambientes=ambientes)

    @app.route('/bens/deletar/<int:id_bem>', methods=['POST'])
    def deletar_bem(id_bem):
        bem = Bem.query.get_or_404(id_bem)
        try:
            db.session.delete(bem)
            db.session.commit()
            flash('Bem deletado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao deletar bem: {e}', 'danger')
        return redirect(url_for('listar_bens'))

    # --- Rotas para Usuários ---
    @app.route('/usuarios')
    def listar_usuarios():
        usuarios = Usuario.query.all()
        return render_template('usuarios/listar.html', usuarios=usuarios)

    @app.route('/usuarios/criar', methods=['GET', 'POST'])
    def criar_usuario():
        if request.method == 'POST':
            tag_rfid = request.form['tag_rfid']
            nome = request.form['nome']
            tipo_usuario = request.form['tipo_usuario']
            matricula_ou_registro = request.form['matricula_ou_registro']
            email = request.form['email']
            telefone = request.form['telefone']

            try:
                novo_usuario = Usuario(
                    tag_rfid=tag_rfid,
                    nome=nome,
                    tipo_usuario=tipo_usuario,
                    matricula_ou_registro=matricula_ou_registro,
                    email=email,
                    telefone=telefone
                )
                db.session.add(novo_usuario)
                db.session.commit()
                flash('Usuário criado com sucesso!', 'success')
                return redirect(url_for('listar_usuarios'))
            except IntegrityError:
                db.session.rollback()
                flash('Erro: A tag RFID, matrícula ou e-mail já existe.', 'danger')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar usuário: {e}', 'danger')
        return render_template('usuarios/criar.html')

    @app.route('/usuarios/editar/<int:id_usuario>', methods=['GET', 'POST'])
    def editar_usuario(id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        if request.method == 'POST':
            usuario.nome = request.form['nome']
            usuario.tipo_usuario = request.form['tipo_usuario']
            usuario.matricula_ou_registro = request.form['matricula_ou_registro']
            usuario.email = request.form['email']
            usuario.telefone = request.form['telefone']

            try:
                db.session.commit()
                flash('Usuário atualizado com sucesso!', 'success')
                return redirect(url_for('listar_usuarios'))
            except IntegrityError:
                db.session.rollback()
                flash('Erro: Matrícula ou e-mail já existe.', 'danger')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar usuário: {e}', 'danger')
        return render_template('usuarios/editar.html', usuario=usuario)

    @app.route('/usuarios/deletar/<int:id_usuario>', methods=['POST'])
    def deletar_usuario(id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        try:
            db.session.delete(usuario)
            db.session.commit()
            flash('Usuário deletado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao deletar usuário: {e}', 'danger')
        return redirect(url_for('listar_usuarios'))

    # --- Rotas para Ambientes ---
    @app.route('/ambientes')
    def listar_ambientes():
        ambientes = Ambiente.query.all()
        return render_template('ambientes/listar.html', ambientes=ambientes)

    @app.route('/ambientes/criar', methods=['GET', 'POST'])
    def criar_ambiente():
        if request.method == 'POST':
            nome_ambiente = request.form['nome_ambiente']
            localizacao = request.form['localizacao']
            tag_rfid_ativo = request.form['tag_rfid_ativo']

            try:
                novo_ambiente = Ambiente(
                    nome_ambiente=nome_ambiente,
                    localizacao=localizacao,
                    tag_rfid_ativo=tag_rfid_ativo
                )
                db.session.add(novo_ambiente)
                db.session.commit()
                flash('Ambiente criado com sucesso!', 'success')
                return redirect(url_for('listar_ambientes'))
            except IntegrityError:
                db.session.rollback()
                flash('Erro: Nome do ambiente ou tag RFID ativa já existe.', 'danger')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar ambiente: {e}', 'danger')
        return render_template('ambientes/criar.html')

    @app.route('/ambientes/editar/<int:id_ambiente>', methods=['GET', 'POST'])
    def editar_ambiente(id_ambiente):
        ambiente = Ambiente.query.get_or_404(id_ambiente)
        if request.method == 'POST':
            ambiente.nome_ambiente = request.form['nome_ambiente']
            ambiente.localizacao = request.form['localizacao']
            ambiente.tag_rfid_ativo = request.form['tag_rfid_ativo']

            try:
                db.session.commit()
                flash('Ambiente atualizado com sucesso!', 'success')
                return redirect(url_for('listar_ambientes'))
            except IntegrityError:
                db.session.rollback()
                flash('Erro: Nome do ambiente ou tag RFID ativa já existe.', 'danger')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar ambiente: {e}', 'danger')
        return render_template('ambientes/editar.html', ambiente=ambiente)

    @app.route('/ambientes/deletar/<int:id_ambiente>', methods=['POST'])
    def deletar_ambiente(id_ambiente):
        ambiente = Ambiente.query.get_or_404(id_ambiente)
        try:
            db.session.delete(ambiente)
            db.session.commit()
            flash('Ambiente deletado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao deletar ambiente: {e}', 'danger')
        return redirect(url_for('listar_ambientes'))

    # --- Rotas para Movimentações ---
    @app.route('/movimentacoes')
    def listar_movimentacoes():
        movimentacoes = Movimentacao.query.order_by(Movimentacao.data_hora.desc()).all()
        return render_template('movimentacoes/listar.html', movimentacoes=movimentacoes)

    # --- Nova Rota para Relatório de Movimentações por Período ---
    @app.route('/movimentacoes/relatorio_periodo', methods=['GET', 'POST'])
    def relatorio_movimentacoes_periodo():
        movimentacoes_filtradas = []
        data_inicio = None
        data_fim = None
        erro_datas = None

        if request.method == 'POST':
            data_inicio_str = request.form.get('data_inicio')
            data_fim_str = request.form.get('data_fim')

            if not data_inicio_str or not data_fim_str:
                erro_datas = "Por favor, preencha ambas as datas para o relatório."
            else:
                try:
                    data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
                    data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()

                    if data_inicio > data_fim:
                        erro_datas = "A data de início não pode ser posterior à data de fim."
                    else:
                        # Para incluir o dia final completo, ajustamos data_fim para o final do dia
                        # Ou, para simplicidade de `date` comparison, filtramos >= data_inicio e <= data_fim
                        movimentacoes_filtradas = Movimentacao.query.filter(
                            and_(
                                Movimentacao.data_hora >= data_inicio,
                                Movimentacao.data_hora <= data_fim
                            )
                        ).order_by(Movimentacao.data_hora.desc()).all()
                        
                        if not movimentacoes_filtradas:
                            flash("Nenhuma movimentação encontrada para o período selecionado.", 'info')

                except ValueError:
                    erro_datas = "Formato de data inválido. Use AAAA-MM-DD."
                except Exception as e:
                    erro_datas = f"Ocorreu um erro ao gerar o relatório: {str(e)}"
        
        return render_template(
            'movimentacoes/relatorio_periodo.html',
            movimentacoes=movimentacoes_filtradas,
            data_inicio=data_inicio,
            data_fim=data_fim,
            erro_datas=erro_datas
        )


    # --- Endpoint para receber dados do leitor RFID ativo ---
    @app.route('/api/rfid_leitura', methods=['POST'])
    def rfid_leitura():
        data = request.json
        if not data:
            return jsonify({'message': 'Nenhum dado JSON fornecido'}), 400

        tag_rfid_passiva_lida = data.get('tag_rfid_passiva')
        tag_rfid_ativa_da_porta = data.get('tag_rfid_ativa_da_porta')
        tipo_movimento = data.get('tipo_movimento') # 'entrada' ou 'saida'

        if not all([tag_rfid_passiva_lida, tag_rfid_ativa_da_porta, tipo_movimento]):
            return jsonify({'message': 'Dados incompletos'}), 400

        try:
            # 1. Identificar o ambiente do leitor RFID ativo
            ambiente_leitor = Ambiente.query.filter_by(tag_rfid_ativo=tag_rfid_ativa_da_porta).first()
            if not ambiente_leitor:
                return jsonify({'message': f'Leitor RFID ativo "{tag_rfid_ativa_da_porta}" não encontrado.'}), 404

            # 2. Verificar se a tag passiva é de um bem ou usuário
            bem = Bem.query.filter_by(tag_rfid=tag_rfid_passiva_lida).first()
            usuario = Usuario.query.filter_by(tag_rfid=tag_rfid_passiva_lida).first()

            if bem:
                tipo_item = 'bem'
                # 3. Atualizar a localização do bem
                if tipo_movimento == 'entrada':
                    bem.id_ambiente_atual = ambiente_leitor.id_ambiente
                # Lógica para saída: o bem pode estar "em trânsito" ou ser movido para 'NULL' ou 'Exterior'
                # Por simplicidade, vamos considerar que 'entrada' atualiza a localização
                db.session.add(bem)
                db.session.commit()
            elif usuario:
                tipo_item = 'usuario'
                # Não atualizamos a localização do usuário diretamente, apenas registramos a movimentação
            else:
                return jsonify({'message': f'Tag RFID passiva "{tag_rfid_passiva_lida}" não encontrada como bem ou usuário.'}), 404

            # 4. Registrar a movimentação
            nova_movimentacao = Movimentacao(
                tag_rfid_item=tag_rfid_passiva_lida,
                tipo_item=tipo_item,
                id_ambiente_leitor=ambiente_leitor.id_ambiente,
                data_hora=datetime.utcnow(),
                tipo_movimentacao=tipo_movimento
            )
            db.session.add(nova_movimentacao)
            db.session.commit()

            return jsonify({'message': 'Movimentação registrada e localização do bem atualizada (se aplicável) com sucesso!'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Erro ao processar leitura RFID: {str(e)}'}), 500