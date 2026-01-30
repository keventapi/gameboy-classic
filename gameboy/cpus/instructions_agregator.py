
def op_87(cpu):
    return cpu.instructions.add.execute_add_a_n('A', 4)

def op_80(cpu):
    return cpu.instructions.add.execute_add_a_n('B', 4)

def op_81(cpu):
    return cpu.instructions.add.execute_add_a_n('C', 4)

def op_82(cpu):
    return cpu.instructions.add.execute_add_a_n('D', 4)

def op_83(cpu):
    return cpu.instructions.add.execute_add_a_n('E', 4)

def op_84(cpu):
    return cpu.instructions.add.execute_add_a_n('H', 4)

def op_85(cpu):
    return cpu.instructions.add.execute_add_a_n('L', 4)

def op_86(cpu):
    return cpu.instructions.add.execute_add_a_n('HL', 8)

def op_c6(cpu):
    return cpu.instructions.add.execute_add_a_n('#', 8)

def op_8f(cpu):
    return cpu.instructions.add.execute_adc_a_n('A', 4)

def op_88(cpu):
    return cpu.instructions.add.execute_adc_a_n('B', 4)

def op_89(cpu):
    return cpu.instructions.add.execute_adc_a_n('C', 4)

def op_8a(cpu):
    return cpu.instructions.add.execute_adc_a_n('D', 4)

def op_8b(cpu):
    return cpu.instructions.add.execute_adc_a_n('E', 4)

def op_8c(cpu):
    return cpu.instructions.add.execute_adc_a_n('H', 4)

def op_8d(cpu):
    return cpu.instructions.add.execute_adc_a_n('L', 4)

def op_8e(cpu):
    return cpu.instructions.add.execute_adc_a_n('HL', 8)

def op_ce(cpu):
    return cpu.instructions.add.execute_adc_a_n('#', 8)

def op_09(cpu):
    return cpu.instructions.add.execute_add_hl_n('BC', 8)

def op_19(cpu):
    return cpu.instructions.add.execute_add_hl_n('DE', 8)

def op_29(cpu):
    return cpu.instructions.add.execute_add_hl_n('HL', 8)

def op_39(cpu):
    return cpu.instructions.add.execute_add_hl_n('SP', 8)

def op_e8(cpu):
    return cpu.instructions.add.execute_add_sp_n(16)

def op_f2(cpu):
    return cpu.instructions.ld.execute_ld_a_FF00_C(True, 8)

def op_e2(cpu):
    return cpu.instructions.ld.execute_ld_a_FF00_C(False, 8)

def op_e0(cpu):
    return cpu.instructions.ld.execute_ld_a_ff00_n(False, 12)

def op_f0(cpu):
    return cpu.instructions.ld.execute_ld_a_ff00_n(True, 12)

def op_0a(cpu):
    return cpu.instructions.ld.ld_a_n('A', 'BC', 8)

def op_1a(cpu):
    return cpu.instructions.ld.ld_a_n('A', 'DE', 8)

def op_fa(cpu):
    return cpu.instructions.ld.ld_a_n('A', 'nn', 16)

def op_3e(cpu):
    return cpu.instructions.ld.ld_a_n('A', '#', 8)

def op_02(cpu):
    return cpu.instructions.ld.ld_n_a('BC', 'A', 8)

def op_12(cpu):
    return cpu.instructions.ld.ld_n_a('DE', 'A', 8)

def op_ea(cpu):
    return cpu.instructions.ld.ld_n_a('nn', 'A', 16)

def op_f8(cpu):
    return cpu.instructions.ld.run_ld_hl_sp_n(12)

def op_01(cpu):
    return cpu.instructions.ld.execute_ld_n_nn('BC', 12)

def op_11(cpu):
    return cpu.instructions.ld.execute_ld_n_nn('DE', 12)

def op_21(cpu):
    return cpu.instructions.ld.execute_ld_n_nn('HL', 12)

def op_31(cpu):
    return cpu.instructions.ld.execute_ld_n_nn('SP', 12)

def op_06(cpu):
    return cpu.instructions.ld.ld_n_nn('B', 8)

def op_0e(cpu):
    return cpu.instructions.ld.ld_n_nn('C', 8)

def op_16(cpu):
    return cpu.instructions.ld.ld_n_nn('D', 8)

def op_1e(cpu):
    return cpu.instructions.ld.ld_n_nn('E', 8)

def op_26(cpu):
    return cpu.instructions.ld.ld_n_nn('H', 8)

def op_2e(cpu):
    return cpu.instructions.ld.ld_n_nn('L', 8)

def op_08(cpu):
    return cpu.instructions.ld.execute_ld_nn_sp(20)

def op_7f(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('A', 'A', 4)

def op_78(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('A', 'B', 4)

def op_79(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('A', 'C', 4)

def op_7a(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('A', 'D', 4)

def op_7b(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('A', 'E', 4)

def op_7c(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('A', 'H', 4)

def op_7d(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('A', 'L', 4)

def op_7e(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('A', 'HL', 8)

def op_40(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('B', 'B', 4)

def op_41(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('B', 'C', 4)

def op_42(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('B', 'D', 4)

def op_43(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('B', 'E', 4)

def op_44(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('B', 'H', 4)

def op_45(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('B', 'L', 4)

def op_46(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('B', 'HL', 8)

def op_47(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('B', 'A', 4)

def op_48(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('C', 'B', 4)

def op_49(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('C', 'C', 4)

def op_4a(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('C', 'D', 4)

def op_4b(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('C', 'E', 4)

def op_4c(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('C', 'H', 4)

def op_4d(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('C', 'L', 4)

def op_4e(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('C', 'HL', 8)

def op_4f(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('C', 'A', 4)

def op_50(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('D', 'B', 4)

def op_51(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('D', 'C', 4)

def op_52(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('D', 'D', 4)

def op_53(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('D', 'E', 4)

def op_54(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('D', 'H', 4)

def op_55(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('D', 'L', 4)

def op_56(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('D', 'HL', 8)

def op_57(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('D', 'A', 4)

def op_58(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('E', 'B', 4)

def op_59(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('E', 'C', 4)

def op_5a(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('E', 'D', 4)

def op_5b(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('E', 'E', 4)

def op_5c(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('E', 'H', 4)

def op_5d(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('E', 'L', 4)

def op_5e(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('E', 'HL', 8)

def op_5f(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('E', 'A', 4)

def op_60(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('H', 'B', 4)

def op_61(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('H', 'C', 4)

def op_62(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('H', 'D', 4)

def op_63(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('H', 'E', 4)

def op_64(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('H', 'H', 4)

def op_65(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('H', 'L', 4)

def op_66(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('H', 'HL', 8)

def op_67(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('H', 'A', 4)

def op_68(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('L', 'B', 4)

def op_69(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('L', 'C', 4)

def op_6a(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('L', 'D', 4)

def op_6b(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('L', 'E', 4)

def op_6c(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('L', 'H', 4)

def op_6d(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('L', 'L', 4)

def op_6e(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('L', 'HL', 8)

def op_6f(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('L', 'A', 4)

def op_70(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('HL', 'B', 8)

def op_71(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('HL', 'C', 8)

def op_72(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('HL', 'D', 8)

def op_73(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('HL', 'E', 8)

def op_74(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('HL', 'H', 8)

def op_75(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('HL', 'L', 8)

def op_36(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('HL', 'N', 12)

def op_77(cpu):
    return cpu.instructions.ld.execute8b_ld_r1_r2('HL', 'A', 8)

def op_f9(cpu):
    return cpu.instructions.ld.execute_ld_sp_hl(8)

def op_3a(cpu):
    return cpu.instructions.ld.execute_ldd(True, 8)

def op_32(cpu):
    return cpu.instructions.ld.execute_ldd(False, 8)

def op_2a(cpu):
    return cpu.instructions.ld.execute_ldi(True, 8)

def op_22(cpu):
    return cpu.instructions.ld.execute_ldi(False, 8)

def op_f1(cpu):
    return cpu.instructions.stack.execute_pop('AF', 12)

def op_c1(cpu):
    return cpu.instructions.stack.execute_pop('BC', 12)

def op_d1(cpu):
    return cpu.instructions.stack.execute_pop('DE', 12)

def op_e1(cpu):
    return cpu.instructions.stack.execute_pop('HL', 12)

def op_f5(cpu):
    return cpu.instructions.stack.execute_push('AF', 16)

def op_c5(cpu):
    return cpu.instructions.stack.execute_push('BC', 16)

def op_d5(cpu):
    return cpu.instructions.stack.execute_push('DE', 16)

def op_e5(cpu):
    return cpu.instructions.stack.execute_push('HL', 16)

def op_97(cpu):
    return cpu.instructions.sub.execute_sub_a_n('A', 4)

def op_90(cpu):
    return cpu.instructions.sub.execute_sub_a_n('B', 4)

def op_91(cpu):
    return cpu.instructions.sub.execute_sub_a_n('C', 4)

def op_92(cpu):
    return cpu.instructions.sub.execute_sub_a_n('D', 4)

def op_93(cpu):
    return cpu.instructions.sub.execute_sub_a_n('E', 4)

def op_94(cpu):
    return cpu.instructions.sub.execute_sub_a_n('H', 4)

def op_95(cpu):
    return cpu.instructions.sub.execute_sub_a_n('L', 4)

def op_96(cpu):
    return cpu.instructions.sub.execute_sub_a_n('HL', 8)

def op_d6(cpu):
    return cpu.instructions.sub.execute_sub_a_n('#', 8)

def op_9f(cpu):
    return cpu.instructions.sub.execute_sbc_a_n('A', 4)

def op_98(cpu):
    return cpu.instructions.sub.execute_sbc_a_n('B', 4)

def op_99(cpu):
    return cpu.instructions.sub.execute_sbc_a_n('C', 4)

def op_9a(cpu):
    return cpu.instructions.sub.execute_sbc_a_n('D', 4)

def op_9b(cpu):
    return cpu.instructions.sub.execute_sbc_a_n('E', 4)

def op_9c(cpu):
    return cpu.instructions.sub.execute_sbc_a_n('H', 4)

def op_9d(cpu):
    return cpu.instructions.sub.execute_sbc_a_n('L', 4)

def op_9e(cpu):
    return cpu.instructions.sub.execute_sbc_a_n('HL', 8)

def op_de(cpu):
    return cpu.instructions.sub.execute_sbc_a_n('#', 8)

def op_a7(cpu):
    return cpu.instructions.alu.execute_and_n('A', 4)

def op_a0(cpu):
    return cpu.instructions.alu.execute_and_n('B', 4)

def op_a1(cpu):
    return cpu.instructions.alu.execute_and_n('C', 4)

def op_a2(cpu):
    return cpu.instructions.alu.execute_and_n('D', 4)

def op_a3(cpu):
    return cpu.instructions.alu.execute_and_n('E', 4)

def op_a4(cpu):
    return cpu.instructions.alu.execute_and_n('H', 4)

def op_a5(cpu):
    return cpu.instructions.alu.execute_and_n('L', 4)

def op_a6(cpu):
    return cpu.instructions.alu.execute_and_n('HL', 8)

def op_e6(cpu):
    return cpu.instructions.alu.execute_and_n('#', 8)

def op_bf(cpu):
    return cpu.instructions.alu.execute_cp_n('A', 4)

def op_b8(cpu):
    return cpu.instructions.alu.execute_cp_n('B', 4)

def op_b9(cpu):
    return cpu.instructions.alu.execute_cp_n('C', 4)

def op_ba(cpu):
    return cpu.instructions.alu.execute_cp_n('D', 4)

def op_bb(cpu):
    return cpu.instructions.alu.execute_cp_n('E', 4)

def op_bc(cpu):
    return cpu.instructions.alu.execute_cp_n('H', 4)

def op_bd(cpu):
    return cpu.instructions.alu.execute_cp_n('L', 4)

def op_be(cpu):
    return cpu.instructions.alu.execute_cp_n('HL', 8)

def op_fe(cpu):
    return cpu.instructions.alu.execute_cp_n('#', 8)

def op_3d(cpu):
    return cpu.instructions.alu.execute_dec_n('A', 4)

def op_05(cpu):
    return cpu.instructions.alu.execute_dec_n('B', 4)

def op_0d(cpu):
    return cpu.instructions.alu.execute_dec_n('C', 4)

def op_15(cpu):
    return cpu.instructions.alu.execute_dec_n('D', 4)

def op_1d(cpu):
    return cpu.instructions.alu.execute_dec_n('E', 4)

def op_25(cpu):
    return cpu.instructions.alu.execute_dec_n('H', 4)

def op_2d(cpu):
    return cpu.instructions.alu.execute_dec_n('L', 4)

def op_35(cpu):
    return cpu.instructions.alu.execute_dec_n('HL', 12)

def op_0b(cpu):
    return cpu.instructions.alu.execute_dec_nn('BC', 8)

def op_1b(cpu):
    return cpu.instructions.alu.execute_dec_nn('DE', 8)

def op_2b(cpu):
    return cpu.instructions.alu.execute_dec_nn('HL', 8)

def op_3b(cpu):
    return cpu.instructions.alu.execute_dec_nn('SP', 8)

def op_3c(cpu):
    return cpu.instructions.alu.execute_inc_n('A', 4)

def op_04(cpu):
    return cpu.instructions.alu.execute_inc_n('B', 4)

def op_0c(cpu):
    return cpu.instructions.alu.execute_inc_n('C', 4)

def op_14(cpu):
    return cpu.instructions.alu.execute_inc_n('D', 4)

def op_1c(cpu):
    return cpu.instructions.alu.execute_inc_n('E', 4)

def op_24(cpu):
    return cpu.instructions.alu.execute_inc_n('H', 4)

def op_2c(cpu):
    return cpu.instructions.alu.execute_inc_n('L', 4)

def op_34(cpu):
    return cpu.instructions.alu.execute_inc_n('HL', 12)

def op_03(cpu):
    return cpu.instructions.alu.execute_inc_nn('BC', 8)

def op_13(cpu):
    return cpu.instructions.alu.execute_inc_nn('DE', 8)

def op_23(cpu):
    return cpu.instructions.alu.execute_inc_nn('HL', 8)

def op_33(cpu):
    return cpu.instructions.alu.execute_inc_nn('SP', 8)

def op_b7(cpu):
    return cpu.instructions.alu.execute_or_n('A', 4)

def op_b0(cpu):
    return cpu.instructions.alu.execute_or_n('B', 4)

def op_b1(cpu):
    return cpu.instructions.alu.execute_or_n('C', 4)

def op_b2(cpu):
    return cpu.instructions.alu.execute_or_n('D', 4)

def op_b3(cpu):
    return cpu.instructions.alu.execute_or_n('E', 4)

def op_b4(cpu):
    return cpu.instructions.alu.execute_or_n('H', 4)

def op_b5(cpu):
    return cpu.instructions.alu.execute_or_n('L', 4)

def op_b6(cpu):
    return cpu.instructions.alu.execute_or_n('HL', 8)

def op_f6(cpu):
    return cpu.instructions.alu.execute_or_n('#', 8)

def op_af(cpu):
    return cpu.instructions.alu.execute_xor_n('A', 4)

def op_a8(cpu):
    return cpu.instructions.alu.execute_xor_n('B', 4)

def op_a9(cpu):
    return cpu.instructions.alu.execute_xor_n('C', 4)

def op_aa(cpu):
    return cpu.instructions.alu.execute_xor_n('D', 4)

def op_ab(cpu):
    return cpu.instructions.alu.execute_xor_n('E', 4)

def op_ac(cpu):
    return cpu.instructions.alu.execute_xor_n('H', 4)

def op_ad(cpu):
    return cpu.instructions.alu.execute_xor_n('L', 4)

def op_ae(cpu):
    return cpu.instructions.alu.execute_xor_n('HL', 8)

def op_ee(cpu):
    return cpu.instructions.alu.execute_xor_n('#', 8)

def op_c4(cpu):
    return cpu.instructions.call.execute_call_cc_nn('NZ', 12)

def op_cc(cpu):
    return cpu.instructions.call.execute_call_cc_nn('Z', 12)

def op_d4(cpu):
    return cpu.instructions.call.execute_call_cc_nn('NC', 12)

def op_dc(cpu):
    return cpu.instructions.call.execute_call_cc_nn('C', 12)

def op_cd(cpu):
    return cpu.instructions.call.execute_call_nn(24)

def op_cb(cpu):
    return cpu.instructions.cb.dispatch(4)

def op_c2(cpu):
    return cpu.instructions.jump.execute_jp_cc_nn('NZ', 12)

def op_ca(cpu):
    return cpu.instructions.jump.execute_jp_cc_nn('Z', 12)

def op_d2(cpu):
    return cpu.instructions.jump.execute_jp_cc_nn('NC', 12)

def op_da(cpu):
    return cpu.instructions.jump.execute_jp_cc_nn('C', 12)

def op_c3(cpu):
    return cpu.instructions.jump.execute_jp_nn('#', 16)

def op_e9(cpu):
    return cpu.instructions.jump.execute_jp_nn('HL', 4)

def op_20(cpu):
    return cpu.instructions.jump.execute_jr_cc_n('NZ', 8)

def op_28(cpu):
    return cpu.instructions.jump.execute_jr_cc_n('Z', 8)

def op_30(cpu):
    return cpu.instructions.jump.execute_jr_cc_n('NC', 8)

def op_38(cpu):
    return cpu.instructions.jump.execute_jr_cc_n('C', 8)

def op_18(cpu):
    return cpu.instructions.jump.execute_jr_n(12)

def op_3f(cpu):
    return cpu.instructions.miscellaneous.execute_ccf(4)

def op_2f(cpu):
    return cpu.instructions.miscellaneous.execute_cpl(4)

def op_27(cpu):
    return cpu.instructions.miscellaneous.execute_daa(4)

def op_f3(cpu):
    return cpu.instructions.miscellaneous.execute_di(4)

def op_fb(cpu):
    return cpu.instructions.miscellaneous.execute_ei(4)

def op_76(cpu):
    return cpu.instructions.miscellaneous.execute_halt(4)

def op_00(cpu):
    return cpu.instructions.miscellaneous.execute_nop(4)

def op_37(cpu):
    return cpu.instructions.miscellaneous.execute_scf(4)

def op_c7(cpu):
    return cpu.instructions.restart.execute_rst_n(0, 16)

def op_cf(cpu):
    return cpu.instructions.restart.execute_rst_n(8, 16)

def op_d7(cpu):
    return cpu.instructions.restart.execute_rst_n(16, 16)

def op_df(cpu):
    return cpu.instructions.restart.execute_rst_n(24, 16)

def op_e7(cpu):
    return cpu.instructions.restart.execute_rst_n(32, 16)

def op_ef(cpu):
    return cpu.instructions.restart.execute_rst_n(40, 16)

def op_f7(cpu):
    return cpu.instructions.restart.execute_rst_n(48, 16)

def op_ff(cpu):
    return cpu.instructions.restart.execute_rst_n(56, 16)

def op_c9(cpu):
    return cpu.instructions.returns.execute_ret(False, 16)

def op_d9(cpu):
    return cpu.instructions.returns.execute_ret(True, 16)

def op_c0(cpu):
    return cpu.instructions.returns.execute_ret_cc('NZ', 8)

def op_c8(cpu):
    return cpu.instructions.returns.execute_ret_cc('Z', 8)

def op_d0(cpu):
    return cpu.instructions.returns.execute_ret_cc('NC', 8)

def op_d8(cpu):
    return cpu.instructions.returns.execute_ret_cc('C', 8)

def op_17(cpu):
    return cpu.instructions.shifts.execute_rla(4)

def op_07(cpu):
    return cpu.instructions.shifts.execute_rlca(4)

def op_1f(cpu):
    return cpu.instructions.shifts.execute_rra(4)

def op_0f(cpu):
    return cpu.instructions.shifts.execute_rrca(4)
